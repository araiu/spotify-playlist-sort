from flask import Flask, jsonify, request
from pymongo import MongoClient
from utils import log_endpoint_calls
import requests
import config
import base64

app = Flask(__name__)

client = MongoClient(config.MONGO_URL)
db = client.test2
users = db.users


@app.route("/")
def hello_world():
    return "Hello, World!🎉"


@app.route("/users", methods=["POST", "GET"])
def create_user():
    if request.method == "GET":
        return jsonify((list(users.find())[0]["data"])), 200
    else:
        user = requests.get(config.API_URL + "users").json()
        users.insert_one(user)
        return jsonify({"success": True}), 200


####
#### Spotify API
####


###
### Helper functions
###
def get_access_token(ID, SECRET):
    """
    Get an access token from the Spotify API
    """
    url = "https://accounts.spotify.com/api/token"
    encoded_credentials = base64.b64encode(f"{ID}:{SECRET}".encode("utf-8")).decode(
        "utf-8"
    )
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = "grant_type=client_credentials"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(
            f"Status code was {response.status_code}, not 200. Response text: {response.text}"
        )
    return response.json()


def get_track_features(track_ids, access_token):
    """
    Get track features from the Spotify API
    Input:
        - track_ids (list of strings)
        - access_token (string)
    """
    response = requests.get(
        f"https://api.spotify.com/v1/audio-features?ids={','.join(track_ids)}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    track_features = {}
    for track in response.json()["audio_features"]:
        track_features[track["id"]] = track

    return track_features


@app.route("/spotify/token")
@log_endpoint_calls
def get_token():
    token = get_access_token(
        config.SPOTIFY["CLIENT_ID"], config.SPOTIFY["CLIENT_SECRET"]
    )
    return jsonify(token), 200


@app.route("/spotify/playlist")
@log_endpoint_calls
def get_playlist():
    token = get_access_token(
        config.SPOTIFY["CLIENT_ID"], config.SPOTIFY["CLIENT_SECRET"]
    )
    playlist_json = requests.get(
        f"https://api.spotify.com/v1/playlists/{config.SPOTIFY['PLAYLSIT_ID']}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    ).json()
    playlist_length = len(playlist_json["tracks"]["items"])
    if request.args.get("output") != "list":
        filtered_playlist = {}
        for item in playlist_json["tracks"]["items"]:
            filtered_playlist[item["track"]["id"]] = {
                "artists": ",".join(
                    artist["name"] for artist in item["track"]["artists"]
                ),
                "name": item["track"]["name"],
            }

        if request.args.get("features") == "true":
            track_features = get_track_features(
                list(filtered_playlist.keys()), token["access_token"]
            )
            for track_id, track in filtered_playlist.items():
                track["features"] = track_features[track_id]
    elif request.args.get("output") == "list":
        filtered_playlist = []
        for item in playlist_json["tracks"]["items"]:
            filtered_playlist.append(
                {
                    "id": item["track"]["id"],
                    "artists": ",".join(
                        artist["name"] for artist in item["track"]["artists"]
                    ),
                    "name": item["track"]["name"],
                }
            )
        # Populate track features
        if request.args.get("features") == "true":
            track_features = get_track_features(
                [track["id"] for track in filtered_playlist],
                token["access_token"],
            )
            for track in filtered_playlist:
                track["features"] = track_features[track["id"]]

    return jsonify(filtered_playlist), 200
