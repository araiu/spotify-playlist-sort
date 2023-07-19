import pytest
import runMe
import config


@pytest.fixture
def app():
    app = runMe.app
    return app


def test_hello(app):
    """Test the hello world route"""
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert "Hello, World!" in response.text


def test_get_access_token(app):
    """Test the get_access_token function"""
    response = app.test_client().get("/spotify/token")
    assert response.status_code == 200
    assert response.json.get("access_token") is not None


def test_get_playlist(app):
    """Test the get_playlist function"""
    response = app.test_client().get("/spotify/playlist")
    assert response.status_code == 200
    key_list_to_check = set(["artists", "name"])
    assert (
        set(  # 0. convert dict_keys to set, as order doesn't matter
            list(response.json.items())[0][  # 1. get list of tuples
                1
            ].keys()  # 2. get the second element of the tuple (the value) and get the keys
        )
        == key_list_to_check
    )


def test_get_playlist_with_features(app):
    """Test the get_playlist function with features"""
    response = app.test_client().get("/spotify/playlist?features=true")
    assert response.status_code == 200
    key_list_to_check = set(["artists", "name", "features"])
    assert set(list(response.json.items())[0][1].keys()) == key_list_to_check


def test_get_playlist_with_features_and_output_list(app):
    """Test the get_playlist function with features and output list"""
    response = app.test_client().get("/spotify/playlist?features=true&output=list")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    key_list_to_check = set(["artists", "name", "id", "features"])
    assert set(response.json[0].keys()) == key_list_to_check
