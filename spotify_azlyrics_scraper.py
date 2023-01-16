import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
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
HEADERS = {'Authorization': 'Bearer {token}'.format(token=access_token)}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# time delay (seconds) for requests made to AZLyrics
DELAY = 5

def get_playlist_data(playlist_id):
    """ Given playlist_id, returns a pandas dataframe of
        the track name, artist(s), and lyrics of each song.
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
            track_info = {'name': item['track']['name'],
                            'artists': [],
                            'lyrics': ''}
            for artist in item['track']['artists']:
                track_info['artists'].append(artist['name'])
            track_info['lyrics'] = scrape_lyrics(track_info['artists'][0],
                                                track_info['name'])
            time.sleep(DELAY) # to prevent being blocked from AZLyrics
            
            data.append(track_info)
    df = pd.DataFrame(data)
    return df

def clean_artist_name(artist_name):
    """ Helper function to format the artist's name
        according to AZLyrics' URLs.
    """
    artist_name = artist_name.lower().replace(' ','')
    artist_name = re.sub(r'[^\w\s]', '', artist_name)
    artist_name = unidecode.unidecode(artist_name)
    return artist_name

def clean_song_name(song_name):
    """ Helper function to format the track's name
        according to AZLyrics' URLs.
    """
    if ('(feat. ' in song_name):
        song_name = song_name[:song_name.find('(feat. ')-1]
    if ('(with ' in song_name):
        song_name = song_name[:song_name.find('(with ')-1]
    song_name = song_name.lower().replace(' ','')
    song_name = re.sub(r'[^\w\s]', '', song_name)
    song_name = unidecode.unidecode(song_name)
    return song_name

def scrape_lyrics(artist, song):
    """ Given a track's (main) artist and name,
        returns the lyrics as a string.
        An empty string is returned if the
        track was not located on AZLyrics.
    """
    artist_name = clean_artist_name(artist)
    song_name = clean_song_name(song)
    
    url = 'https://www.azlyrics.com/lyrics/'+ artist_name + '/' + song_name + '.html'
    page = requests.get(url)
    if page.status_code != 200:
        print("Could not reach", url)
        return ""
    html = BeautifulSoup(page.text, 'html.parser')
    lyric = html.select_one(".ringtone ~ div").get_text(strip=True, separator="\n")

    return lyric