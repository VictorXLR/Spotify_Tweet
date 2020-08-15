import os
import pickle
from time import sleep

import tekore as tk
from tekore.model import CurrentlyPlaying

from functions import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SECRET_CLIENT_ID,
    TOKEN_PICKLED,
    get_last_tweet,
    send_tweet,
)

token = None
TIME_INTERVAL = 180
configuration = (SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_CLIENT_ID, SPOTIFY_REDIRECT_URI)


twt_msg = """
I am listening to {} by {}

{}"""

if os.path.exists("./token.cred"):
    with open("token.cred", "rb") as dump:
        token = pickle.load(dump)
else:
    token = tk.prompt_for_user_token(*configuration, scope=tk.scope.every)
    with open("token.cred", "wb") as file:
        pickle.dump(token, file, pickle.HIGHEST_PROTOCOL)


def countdown(t=TIME_INTERVAL) -> None:
    while t:
        mins, secs = divmod(t, 60)
        time_format = "{:02d}:{:02d}".format(mins, secs)
        print(time_format, end="\r")
        sleep(1)
        t -= 1
    return


def generate_tweet() -> str:
    trk_artists = ""
    try:
        spotify = tk.Spotify(token)
        curr_playing: CurrentlyPlaying = spotify.playback_currently_playing()
        curr_track = curr_playing.item
        num_artists = len(curr_track.artists)
        trk_name = curr_playing.item.name
        spotify_url = curr_track.external_urls["spotify"]

        for val in curr_track.artists:
            trk_artists += val.name + " & "

        trk_artists = trk_artists[:-2]
        print(trk_name)
        print(num_artists)
        print(trk_artists)
        print(spotify_url)
        msg = twt_msg.format(trk_name, trk_artists, spotify_url)
        return msg
    except Exception as e:
        print("No Song Playing")


if __name__ == "__main__":
    message = generate_tweet()
    send_tweet(message)
    while True:
        countdown()
        last_tweet = get_last_tweet()
        message = generate_tweet()
        print(message)
        if message != last_tweet:
            send_tweet(message)
        else:
            print("You have tweeted this before")
            countdown(30)
