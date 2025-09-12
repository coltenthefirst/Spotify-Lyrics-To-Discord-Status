import json
import time # time-python - idk if pip installing time-python is needed. i think it comes with python but idk
import requests
from spotify_lyrics import SpotifyLyricsManager

# thanks to @the_real_universal_cat for this method <3
def change_status(token, message, emoji_name, emoji_id):
    header = {'authorization': token}
    payload = {"custom_status": {"text": message}}
    if emoji_id:
        payload["custom_status"].update({"emoji_name": emoji_name, "emoji_id": emoji_id})
    else:
        payload["custom_status"]["emoji_name"] = emoji_name
    r = requests.patch("https://discord.com/api/v10/users/@me/settings", headers=header, json=payload, timeout=2)
    return r.status_code == 200


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def main():
    config = load_config()
    token = config["token"]
    
    spotify_manager = SpotifyLyricsManager(
        client_id=config["spotify_client_id"],
        client_secret=config["spotify_client_secret"],
        redirect_uri=config["spotify_redirect_uri"],
        early_delay_ms=config.get("lyrics_early_delay_ms", 700)
    )

    last_status = None
    last_track_id = None

    while True:
        try:
            track_info = spotify_manager.get_current_track()
            if track_info:
                track_id = track_info['track_id']
                
                if track_id != last_track_id:
                    last_track_id = track_id
                    last_status = None
                
                current_lyric = spotify_manager.get_current_lyric(track_info)
                if current_lyric:
                    status = current_lyric
                    emoji_name = f"{track_info['artist'][:15]}..."
                    
                    if status != last_status:
                        print(f"{time.strftime('%I:%M %p')} {status}")
                        change_status(token, status, emoji_name, None)
                        last_status = status
                elif current_lyric is None and spotify_manager.last_lyric is not None:
                    time.sleep(0.05)
                    continue
                else:
                    status = spotify_manager.get_fallback_track_info(track_info)
                    emoji_name = "♪"
                    
                    if status != last_status:
                        print(f"{time.strftime('%I:%M %p')} {status}")
                        change_status(token, status, emoji_name, None)
                        last_status = status
            else:
                if last_track_id is not None:
                    last_track_id = None
                    last_status = None
                
                status = "Spotify Lyrics To Discord Status By @unknowingly_exists" # don't fw this
                emoji_name = "🎵"
                
                if status != last_status:
                    print(f"{time.strftime('%I:%M %p')} {status}")
                    change_status(token, status, emoji_name, None)
                    last_status = status

            time.sleep(0.05)
        except KeyboardInterrupt: # placed here to get rid of the stupid error message
            print("\nStopped")
            break
        except Exception:
            time.sleep(0.5)

if __name__ == "__main__":
    main()