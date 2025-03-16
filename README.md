# Spotify Artist Tracker
This script can be used to create playlists featuring new releases from specified artists. When run it gets all new tracks since the last run (or start of month) and populates a new playlist.

## Prerequisites
### Create Client ID and Client Secret
1. Log into Spotify Developer Dashboard: https://developer.spotify.com/dashboard
2. Click the *Create App* button and fill in the following information:
    - App Name: Any name 
    - App Description: Any description
    - Redirect URI:  http://127.0.0.1:3000
3. From the dashboard select the app just created
4. Click the *Settings* button 
5. **client id** and **client secret** can be found here
6. Install all required libraries with **python -m pip install -r requirements.txt**

### Fill in info.json with your personalized information
1. Rename **sampleInfo.json** to **info.json**
2. Fill in the **clientId** and **clientSecret** fields
3. Following the format of the artists list, create a personalized list of artists

## Running the app
1. Python must be installed on the device
2. App can be run from the command line using the command **python3 trackFavouriteArtists.py**
