import json
import base64
from requests import get, post
from datetime import datetime, timedelta

def get_token(client_id, client_secret):
   auth_string = client_id + ":" + client_secret
   auth_bytes = auth_string.encode("utf-8")
   auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

   url = "https://accounts.spotify.com/api/token"
   headers = {
      "Authorization" : "Basic " + auth_base64,
      "Content-Type": "application/x-www-form-urlencoded"
   }
   data = {"grant_type": "client_credentials"}
   result = post(url, headers=headers ,data=data)
   json_result = json.loads(result.content)
   token = json_result["access_token"]
   return token

def get_auth_headers(token):
   return {"Authorization": "Bearer " + token}



def get_artist_music_since_last_run(headers, date, artist):
  url = "https://api.spotify.com/v1/search"

  year_end = datetime.now().year
  if (date):
     date = datetime.strptime(date, '%Y-%m-%d')
     year_start =   date.year
  else :
     date = datetime.today()
     year_start = datetime.now().year - 1
     date = (date - timedelta(days=31))

  queryUrl = url + f"?q=artist%3A{artist}+year%3A{year_start}-{year_end}&type=track&limit=50"
  result = get(queryUrl, headers=headers)
  result_json = json.loads(result.content)["tracks"]["items"]

  tracks = dict()

  for result in result_json:
     date_released = datetime.strptime(result.get('album').get('release_date'), '%Y-%m-%d')
     name = result.get('name')
     if date_released > date:
        tracks[name] = result.get('uri')
        print(result.get('name'))


  return tracks




def main():
   info_file = open("info.json", 'r+')
   info_json = json.load(info_file)

   token = get_token(info_json['clientId'], info_json['clientSecret'])
   headers = get_auth_headers(token)

   artists = info_json["artists"]
   date = info_json["lastRun"]
   
   tracks = dict()
   for artist in artists:
    tracks.update(get_artist_music_since_last_run(headers, date, artist))




   # info_json["lastRun"] = datetime.today().strftime('%Y-%m-%d')
   # info_file.seek(0)
   # json.dump(info_json, info_file, ensure_ascii=False, indent=4)
   info_file.close()

if __name__ == "__main__":
    main()

# goal: get songs since x by all artists I specify
# steps
# 1. get list of artists  x 
# 2. for each artist: 
#     a. search for tracks in last 1-2 years x
#         eg. q=artist:Sammy Virji year:2025 // https://api.spotify.com/v1/search?q=artist%3ASammy+Virji+year%3A2025&type=track
#     b. filter tracks by release date since x 
# 3. create playlist
# 4. add all songs to playlist
