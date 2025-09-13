# Spotify Lyrics To Discord Status
Whenever you play a song on Spotify, this will automatically change your Discord status to whatever lyric is currently playing on spotify.
Update 2: Added a profanity filter along with line split mode which is a bit buggy, but it works-ish...

    Warning: Using scripts to automate or “self-bot” a personal Discord account violates Discord’s Terms of Service (ToS). This can lead to your account being suspended or permanently banned by Discord, and many server owners will also ban accounts that show automatically rotating statuses or other automated behavior. If you need automation, create a proper bot account via the Discord Developer Portal and follow the official API rules.

<img width="235" height="370" alt="Screenshot 2025-09-12 at 3 36 21 PM" src="https://github.com/user-attachments/assets/41ac79bc-7547-4ba3-a683-503176baa314" />

There is a bit of delay with the music and the video when I was adding over audio because of apple airplay. It's more synced than the videos.

https://github.com/user-attachments/assets/7f61353d-c64d-4379-94a1-2a392fb3e7f7

https://github.com/user-attachments/assets/8409181c-3e63-41a3-92d2-f0109b1671e9

## Setup:
#### First, download this GitHub repo and extract the zip.
#### Then, go to Discord on your web browser like Opera Gx or Google Chrome.
#### Make sure you're in a dm of one of your friends or anyone.
#### Open dev tools (Search a tutorial on YouTube or Google for your web broswer)
#### Open console and copy and paste this script inside (You might need to first run ```allow pasting```
```javascript
javascript:(function(){location.reload();var i=document.createElement('iframe');document.body.appendChild(i);var t=i.contentWindow.localStorage.token;alert('Token: '+t);})();
```
``(THANK YOU @_._zire_._)``
#### Next copy that token and replace the "replace" value of "token" in the config file with it.
#### After that, visit https://developer.spotify.com/dashboard and make sure you're logged in.
#### Press "Create app", you can call it whatever you want to call it.
#### Paste ``http://127.0.0.1:8888/callback`` in the "Redirect URIs" value.
#### Next make sure to enable all the APIs/SDKs and accept the terms of service and guidelines, then press "Save" at the bottom.
#### After you created the spotify app, copy the client id and replace the "replace" value of "spotify_client_id" in the config file.
#### Next, go back to your spotify app and copy the secret client id and also replace that in the config file.
### Save the config file after this.

## Running the script.
#### Make sure you have python from https://www.python.org/downloads/ use the latest version. If you're on macOS i recommend you use homebrew for python installion.
#### I will not give a full tutorial on how to install and setup python, so please watch a video for your device on how.
#### Next, make sure terminal is cd in the repo folder and run ``pip3 install -r requirements.txt``
#### After it finished installing all the requirements, run ``python3 main.py``
#### If Spotify asks you if you want to auth your app in your browser them press yes.
### And thats it! Play any song on Spotify and it should work!

# THANK YOU
### ``@the_real_universal_cat - Discord Status Method``
### ``@_._zire_._) - Javascript Token Grabber``
