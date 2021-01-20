import os
from time import sleep

import tekore as tk
from tekore.model import CurrentlyPlaying

from functions import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SECRET_CLIENT_ID,
    get_last_tweet,
    send_tweet,
)

File = "token.cfg"
token = None
TIME_INTERVAL = 180
conf = (SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_CLIENT_ID, SPOTIFY_REDIRECT_URI)


twt_msg = """
I am listening to {} by {}

{}"""

# This lines dump the credentials to a file called token.cred in order for the
# refeshing token to work anytime its run. Basically, if the file exists the app
# will not ask for you to login.
if os.path.exists(File):
    conf = tk.config_from_file(File, return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])
else:
    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    tk.config_to_file(File, conf + (token.refresh_token,))


# function to modify time interval for check operation, right now its
# 180 seconds, but depending on your usecase, can be modified.
def countdown(t=TIME_INTERVAL) -> None:
    while t:
        mins, secs = divmod(t, 60)
        time_format = "{:02d}:{:02d}".format(mins, secs)
        print(time_format, end="\r")
        sleep(1)
        t -= 1
    return


# Takes data from spotify API and uses it to compose a string to be tweeted out
# could have added other functionality but it works fine for now.
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


# Runs forever :), can operate on a headless server on a tmux instance and
# provides enough checking to carry itself.
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
