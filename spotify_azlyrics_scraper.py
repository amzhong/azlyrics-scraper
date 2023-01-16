import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import random
import unidecode

# locate your own client id and client secret at https://developer.spotify.com/dashboard/
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

# post request and save access token
auth_response = requests.post('https://accounts.spotify.com/api/token', 
    {'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET}).json()
access_token = auth_response['access_token']
HEADERS = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

def get_playlist_data(playlist_id):
    """ Given playlist_id, returns a pandas dataframe
        of the track name and artist(s) of each song.
    """
    playlist_length = 50
    data = [] # will store each track's name and artists
    counter = 0 # counter for the number of tracks appended to data

    while counter < playlist_length:
        playlist_request = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks',
                                        headers = HEADERS,
                                        params = {'limit': 50, 'offset': counter})
        if (playlist_request.status_code != 200):
            print("Could not fetch playlist.")
            return
        playlist = playlist_request.json()
        if (counter == 0):
            playlist_length = playlist['total']
        counter = min(counter + 50, playlist_length) # update counter

        # iterate through tracks in playlist
        for item in playlist['items']:
            track_info = {'name': item['track']['name'], 'artists': []}
            for artist in item['track']['artists']:
                track_info['artists'].append(artist['name'])
            data.append(track_info)
    df = pd.DataFrame(data)
    return df