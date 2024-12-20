import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tidalapi
from flask import Flask, request, redirect, jsonify
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, TIDAL_USERNAME, TIDAL_PASSWORD

app = Flask(__name__)

# Spotify authentication
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope="user-library-read playlist-read-private")

sp = spotipy.Spotify(auth_manager=sp_oauth)

# Tidal authentication
def printer(message):
    print(message)

session = tidalapi.Session()
session.login_oauth_simple(fn_print=printer)

token_type = session.token_type
access_token = session.access_token
refresh_token = session.refresh_token # Not needed if you don't care about refreshing
expiry_time = session.expiry_time

print(session.load_oauth_session(token_type, access_token, refresh_token, expiry_time))

@app.route('/')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args.get('code'))
    spotify_data = get_spotify_data()
    import_to_tidal(spotify_data)
    return jsonify(spotify_data)

def get_spotify_data():
    playlists = sp.current_user_playlists()
    all_data = []
    for playlist in playlists['items']:
        playlist_data = {
            'name': playlist['name'],
            'tracks': []
        }
        tracks = sp.playlist_tracks(playlist['id'])
        for item in tracks['items']:
            track = item['track']
            track_data = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name']
            }
            playlist_data['tracks'].append(track_data)
        all_data.append(playlist_data)
    return all_data

def import_to_tidal(data):
    for playlist in data:
        tidal_playlist = session.user.create_playlist(playlist['name'], 'Imported from Spotify')
        for track in playlist['tracks']:
            search_results = session.search(f"{track['name']} {track['artist']}", [tidalapi.Track])
            top_hit = search_results['top_hit']
            if not top_hit:
                print(f"\tNo results found for track: {track['name']} by {track['artist']} from album {track['album']}")
                continue
            
            tidal_playlist.add([top_hit.id])

if __name__ == "__main__":
    app.run(port=8000)