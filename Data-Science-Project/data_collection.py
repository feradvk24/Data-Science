import requests
import re
from bs4 import BeautifulSoup
from requests.models import Response

class AZLyrics:
    def __init__(self, artist, song):
        self.artist = artist.replace(" ", "").lower()
        self.song = song.replace(" ", "").lower()
        self.lyrics = None
        
    def parse_text(self, text):
        accent_map = str.maketrans(
        'àáâãäåèéêëéìíîïòóôõöùúûüýÿ',
        'aaaaaaeeeeeiiiiooooouuuuyy'
        )
        text = text.translate(accent_map)
        if text.startswith('The '):
            text = text[4:]  # Remove the first 4 characters (i.e., "The "), as the AZLyrics url does not contain it
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.strip())

        cleaned = cleaned.lower()
        return cleaned

    def url(self):
        return "https://www.azlyrics.com/lyrics/{}/{}.html".format(self.parse_text(self.artist), self.parse_text(self.song))
    

    def scrape(self):
        URL = self.url()
        response = requests.get(URL)
        lyrics = None

        if response.ok:
            lyrics = self.scrape_lyrics(response)

        return lyrics
    
    def scrape_lyrics(self, r):
        dom = BeautifulSoup(r.text, "html.parser")
        body = dom.body
        divs = body.find_all(
                "div", {"class": "col-xs-12 col-lg-8 text-center"}
        )[0]

        target = {0: 0}

        for i, d in enumerate(divs):
            try:
                query = d.find_all("br")
                n_br = len(query)
                if n_br > list(target.values())[0]:
                    target = {i: n_br}
            except:
                pass

        target = list(target.keys())[0]
        lyrics = list(divs.children)[target].text

        return lyrics
    

    
def get_track_details_by_name(empty_value_index, track_name, main_artist_name, sp):
    # Build the search query string
    query = f"track:{track_name} artist:{main_artist_name}"
    
    # Search for the track by name and artist(s)
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        # Get the first track's information
        track = results['tracks']['items'][0]
        track_id = track['id']
        
        # Get the artist's ID from the track
        artist_id = track['artists'][0]['id']
        
        # Get artist information to retrieve genres
        artist = sp.artist(artist_id)
        genres = artist['genres']
        
        # Get audio features of the track
        audio_features = sp.audio_features(track_id)[0]
        
        # Combine the data in the specified order
        track_data = {
            'index_empty_val': empty_value_index,
            'spotify_genre': genres,
            'track_duration_s': track['duration_ms'] / 1000,  # Convert to seconds
            'explicit_track': track['explicit'],
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'mode': audio_features['mode'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo'],
            'spotify_popularity': track['popularity'],
            'main_artist': track['artists'][0]['name'],
            'song': track['name'],
        }
        
        return track_data
    else:
        return None


def get_artists(artist_str, main_only = True):
     # Replace common multi-character delimiters with a comma
    artist_str = artist_str.replace(' Featuring ', ',')
    artist_str = artist_str.replace(' featuring ', ',')
    artist_str = artist_str.replace(' & ', ',')
    artist_str = artist_str.replace(' + ', ',')
    artist_str = artist_str.replace(' And ', ',')
    artist_str = artist_str.replace(' Feat. ', ',')
    artist_str = artist_str.replace(' ft. ', ',')
    artist_str = artist_str.replace(' With ', ',')
    
    if main_only == True:
        # Split on commas and take the first part
        return artist_str.split(',')[0].strip()
    else:
        return artist_str.split(',')