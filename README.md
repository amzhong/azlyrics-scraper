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

To find the playlist ID of a playlist, click the (...) button, go down to "Share", hold down the option key (Mac) / Alt key (Windows), and click on the "Copy Spotify URI" option that should appear. This will give you something like

## Usage
