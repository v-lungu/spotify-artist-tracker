import json
import base64
from requests import post

msg = "Roll a dice!"
print(msg)

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



def get_artist_music_since_last_run(token, date, artist):
  print("helli")
  return ["hello"]




def main():
   info_file = open('info.json')
   info_json = json.load(info_file)

   token = get_token(info_json["clientId"], info_json["clientSecret"])
   headers = get_auth_headers(token)

   artists = info_json["artists"]
   date = info_json["lastRun"]
   for artist in artists:
    music = get_artist_music_since_last_run(token, date, artist)





   info_file.close()

if __name__ == "__main__":
    main()

# goal: get songs since x by all artists I specify
# steps
# 1. get list of artists 
# 2. for each artist: 
#     a. search for tracks in last 1-2 years
#         eg. q=artist:Sammy Virji year:2025 // https://api.spotify.com/v1/search?q=artist%3ASammy+Virji+year%3A2025&type=track
#     b. filter tracks by release date since x 
