import json
import base64
import random
import string
from requests import get, post
from hashlib import sha256
import webbrowser
from datetime import datetime, timedelta

def get_token(client_id):
   verifier = ''.join(random.choices(string.ascii_letters+ string.digits, k=64))
   challenge = base64.urlsafe_b64encode(
        sha256(verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
   
   url_auth = 'https://accounts.spotify.com/authorize'
   data_auth = {'client_id': client_id}
   data_auth['response_type'] = 'code'
   data_auth['redirect_uri'] = 'http://127.0.0.1:3000'
   data_auth['code_challenge_method'] = 'S256'
   data_auth['code_challenge'] = challenge
   data_auth['scope'] = 'playlist-modify-public playlist-modify-private'

   result_auth = get(url=url_auth, params=data_auth)
   webbrowser.open(result_auth.url)

   code = input('What is the code: ')

   url_token = 'https://accounts.spotify.com/api/token'
   data_token = {'client_id': client_id}
   data_token['grant_type'] = 'authorization_code'
   data_token['redirect_uri'] = 'http://127.0.0.1:3000'
   data_token['code'] = code
   data_token['code_verifier'] = verifier

   headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
   }

   result_token = post(url=url_token, headers=headers, data=data_token)
   json_result_token = json.loads(result_token.content)
   token = json_result_token['access_token']
   return token


def get_auth_headers(token):
   return {"Authorization": "Bearer " + token}


def get_artist_music_since_last_run(headers, date, artist):
  url = 'https://api.spotify.com/v1/search'

  year_end = datetime.now().year
  if (date):
     date = datetime.strptime(date, '%Y-%m-%d')
     year_start =   date.year
  else :
     date = datetime.today()
     year_start = datetime.now().year - 1
     date = (date - timedelta(days=31))

  queryUrl = url + f'?q=artist%3A{artist}+year%3A{year_start}-{year_end}&type=track&limit=50'
  result = get(queryUrl, headers=headers)
  result_json = json.loads(result.content)['tracks']['items']

  tracks = dict()

  for result in result_json:
     date_released = datetime.strptime(result.get('album').get('release_date'), '%Y-%m-%d')
     name = result.get('name')
     if date_released >= date:
        tracks[name] = result.get('uri')

  return tracks


def get_user_id(headers):
   url = 'https://api.spotify.com/v1/me'
   result = get(url=url, headers=headers)
   json_result = json.loads(result.content)
   return json_result['id']


def create_playlist(headers, last_run):
   user_id = get_user_id(headers)
   url =  'https://api.spotify.com/v1/users/' + user_id + '/playlists'
   headers['Content-Type'] = 'application/json'
   if not last_run:
     last_run = (datetime.today() - timedelta(days=31)).strftime('%Y-%m-%d')

   data = {'name': 'New Music Since ' + last_run}
   data['description'] = 'Playlist filled with new songs since the script last ran'
   data['public'] = 'false'

   result = post(url=url, headers=headers, json=data)
   json_result = json.loads(result.content)
   return json_result['id']


def populate_playlist(headers, playlist_id, tracks):
   url =  'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'
   
   data = {'position': '0'}
   data['uris'] = ', '.join(repr(x) for x in tracks.values())
   data['uris'] = list(tracks.values())
   
   result = post(url=url, headers=headers, json=data)
   json_result = json.loads(result.content)
   print(json_result)


def main():
   info_file = open('info.json', 'r+')
   info_json = json.load(info_file)

   client_id = info_json['clientId']
   last_run = info_json['lastRun']
   artists = info_json['artists']

   token = get_token(client_id)
   headers = get_auth_headers(token)

   tracks = dict()
   for artist in artists:
      tracks.update(get_artist_music_since_last_run(headers, last_run, artist))

   playlist_id = create_playlist(headers, last_run)
   populate_playlist(headers, playlist_id, tracks)

   info_json['lastRun'] = datetime.today().strftime('%Y-%m-%d')
   info_file.seek(0)
   json.dump(info_json, info_file, ensure_ascii=False, indent=4)
   info_file.close()

if __name__ == '__main__':
    main()

