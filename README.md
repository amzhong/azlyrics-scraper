# azlyrics-scraper
Given the playlist ID of a (public) Spotify playlist, scrapes AZLyrics for the lyrics to each track.

This is an alternative to [lyricsgenius](https://github.com/johnwmillr/LyricsGenius), which scrapes Genius instead of AZLyrics. Genius does have a slightly larger database, however lyrics scraped using lyricsgenius tend to be "dirtier" than using AZLyrics.

## Getting started
### Dependencies
- requests
- pandas
- bs4
- re
- time
- unidecode
### Spotify API
Head over to https://developer.spotify.com/dashboard/ and "Create An App" to get your client id and client secret needed to make API calls.

To locate the playlist ID of a playlist, click the (...) button, go down to "Share", hold down the option key (Mac) / Alt key (Windows), and click on the "Copy Spotify URI" option that should appear. This will give you something like _spotify:playlist:37i9dQZF1DX2UgsUIg75Vg_; the `playlist_id` in this case would be _37i9dQZF1DX2UgsUIg75Vg_.

## Usage
First replace `CLIENT_ID` and `CLIENT_SECRET` with your own, then import the file:
```
from spotify_azlyrics_scraper import *
```
To search for the lyrics to a single song, you only need the name of the song and the name of the artist (just the first artist listed, if there are multiple). This will return the lyrics as a string, where each line of the song is separated by `\n`:
```
lyrics = scrape_lyrics('SZA', 'Good Days')
```
If you would like the lyrics to all the songs within a Spotify playlist, then you only need the playlist ID. This will return the playlist data as a pandas DataFrame with each track's name (string), artists (list of strings), and lyrics (string):
```
playlist_data = get_playlist_data('37i9dQZF1DX2UgsUIg75Vg')
```
