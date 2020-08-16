import os
import tweepy
from dotenv import load_dotenv

load_dotenv(verbose=True)

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")


SPOTIFY_USERNAME = os.getenv("SPOTIFY_USERNAME")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_CLIENT_ID = os.getenv("SPOTIFY_SECRET_CLIENT_ID")
REMOTE_SPOTIFY_REDIRECT_URI = os.getenv("REMOTE_SPOTIFY_REDIRECT_URI")
SPOTIFY_REDIRECT_URI = REMOTE_SPOTIFY_REDIRECT_URI

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
username = CLIENT_ID
user = api.get_user(username)


def send_tweet(msg) -> bool:
    try:
        api.update_status(msg)
        print("Tweet sucessfully sent")
        return True
    except Exception as e:
        print(e)
        return False


def get_last_tweet():
    tweet = api.user_timeline(id=username, count=1)[0]
    return tweet.text


if __name__ == "__main__":
    tweet = input("Nel >")
    api.update_status(tweet)
