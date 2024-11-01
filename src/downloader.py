import subprocess
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config_manager import load_decrypted_credentials


download_dir = os.path.join(os.path.dirname(__file__), "downloads")


def download_track(track_name):
    os.makedirs(download_dir, exist_ok=True)
    cmd = [
        "yt-dlp", "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3",
        "--output", f"{os.path.join(download_dir, track_name)}.%(ext)s",
        f"ytsearch:{track_name}"
    ]
    subprocess.run(cmd)


def download_playlist(playlist_id):
    client_id, client_secret = load_decrypted_credentials()
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    
    try:
        playlist = sp.playlist_tracks(playlist_id)
        tracks = [item['track']['name'] + ' ' + item['track']['artists'][0]['name'] for item in playlist['items']]
        
        print(f"Found {len(tracks)} tracks in the playlist.")
        for track in tracks:
            print(f"Downloading {track}...")
            download_track(track)
        print("All downloads complete!")
    except Exception as e:
        print(f"An error occurred: {e}")
