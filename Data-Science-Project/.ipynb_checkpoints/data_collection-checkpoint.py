import requests
import re
from bs4 import BeautifulSoup
from requests.models import Response

    
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
    
    
def remove_stopwords(word_list, stop_words):
    return [word for word in word_list if word.lower() not in stop_words]