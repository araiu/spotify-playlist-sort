# Title TBD

### How to run this
1. Create virtual environment and activate it
```bash
python3 -m venv .venv && source .venv/bin/activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the app
```bash
python3 runMe.py
```

### External dependencies
* MongoDB deployed on [Railway.app](https://railway.app)
* Spotify API credentials required


### Github multiple account management
_Not really needed, but helpful_

```bash
git remote set-url origin https://$USER@github.com/$USER/$REPO_NAME.git
# git push after setting remote url will prompt for password. GH Token is good enough

# Update name and email
git config user.name $NAME
git config user.email $EMAIL

# Check config for this repo
git config --get
git config --global --get # Check if we broke anything in the global config

# Reset the author with whatever we have configured now
git commit --amend --no-edit --reset-author 
```
