import spotipy
import spotipy.exceptions
from spotipy.oauth2 import SpotifyOAuth
import requests
import time # time-python
import re
from typing import Optional, Dict, List, Tuple

class SpotifyLyricsManager:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, early_delay_ms: int = 700):
        self.current_track_id = None
        self.current_lyrics = []
        self.last_lyric = None
        self.lyrics_index = 0
        self.early_delay_ms = early_delay_ms
        
        scope = "user-read-currently-playing user-read-playback-state"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache"
        ))


    def get_current_track(self) -> Optional[Dict]:
        try:
            current_track = self.sp.current_playback()
            if current_track and current_track['is_playing'] and current_track['item']:
                return {
                    'track_id': current_track['item']['id'],
                    'track_name': current_track['item']['name'],
                    'artist': current_track['item']['artists'][0]['name'],
                    'progress_ms': current_track['progress_ms'] or 0,
                    'duration_ms': current_track['item']['duration_ms'] or 0
                }
        except Exception:
            pass
        return None


    # lrclib is kinda shiii but it's free and it works so...
    # i might replace in the future or add another api for fallback
    def get_lrclib_lyrics(self, track_name: str, artist: str, duration_s: int) -> List[Tuple[int, str]]:
        try:
            url = "https://lrclib.net/api/search"
            params = {
                'track_name': track_name,
                'artist_name': artist,
                'duration': duration_s
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json()
                if results and len(results) > 0:
                    syncedLyrics = results[0].get('syncedLyrics')
                    if syncedLyrics:
                        return self.parse_lrc_lyrics(syncedLyrics)
        except Exception:
            pass
        return []


    def parse_lrc_lyrics(self, lrc_content: str) -> List[Tuple[int, str]]:
        lyrics = []
        lines = lrc_content.strip().split('\n')
        
        for line in lines:
            match = re.match(r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)', line)
            if match:
                minutes, seconds, centiseconds, text = match.groups()
                timestamp_ms = (int(minutes) * 60 + int(seconds)) * 1000 + int(centiseconds) * 10
                lyrics.append((timestamp_ms, text.strip()))
        
        return sorted(lyrics)


    def get_current_lyric(self, track_info: Dict) -> Optional[str]:
        track_id = track_info['track_id']
        progress_ms = track_info['progress_ms']
        
        if track_id != self.current_track_id:
            print(f"Fetching lyrics for: {track_info['artist']} - {track_info['track_name']}")
            
            duration_s = track_info.get('duration_ms', 0) // 1000
            self.current_lyrics = self.get_lrclib_lyrics(
                track_info['track_name'], 
                track_info['artist'],
                duration_s
            )
            
            self.current_track_id = track_id
            self.last_lyric = None
            self.lyrics_index = 0
            
            if self.current_lyrics:
                print(f"(lrclib) found {len(self.current_lyrics)} lyrics")
            else:
                print("(lrclib) no lyrics found") # fallback api later - else lyrics doesn't publicly exist soo...
        
        if not self.current_lyrics:
            return None
        
        early_progress_ms = progress_ms + self.early_delay_ms
        
        current_lyric = None
        for i, (timestamp_ms, lyric_text) in enumerate(self.current_lyrics): # lyric_text is the lyric itself for notes
            if timestamp_ms <= early_progress_ms:
                current_lyric = lyric_text
                self.lyrics_index = i
            else:
                break
        
        current_lyric = current_lyric if current_lyric and current_lyric.strip() else None # i somehow had a stroke when writing this lmao
        
        if current_lyric != self.last_lyric:
            self.last_lyric = current_lyric
            return current_lyric
        
        return None


    def get_fallback_track_info(self, track_info: Dict) -> str:
        return f"{track_info['artist']} - {track_info['track_name']}"