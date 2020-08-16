## Spotify Tweet


This is an update to my Spotify_Tweet application which read the currently playing song by utilizing the win32 api to read the title of the window directory.

This update is neater, spanning 2 functions and utilizing the spotify API to get the currently playing songs. 

### Dependencies
```
pip install -r requirements.txt
```
- Teokore - Interacting with the Spotify API to get currently playing credentials
- Tweepy - Interacting with the Twitter API to get last tweets and send a current Tweet
- python-dotenv - Reading enviroment variables storred in a files



# Running 
```
python app.py
```
ensure the enviroment variables required in `functions.py` are stored either in a `.env` file 
