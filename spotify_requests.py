import requests
from spotify_auth import get_auth_header, get_token
import json


class SpotifyRequests:

        def __init__(self,token):
                self.token=token

        def return_artists(self,arr):
                        return arr['name']

        def get_tracks_and_artists(self,playlistId):
                limit=20
                items=[]
                total=json.loads(requests.get(f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?market=GB&limit=1&offset=1",
                                                headers=get_auth_header(self.token)).content)['total']
                pages=(total//limit)+1
                for i in range(pages):
                        my_playlist= requests.get(f"https://api.spotify.com/v1/playlists/{playlistId}/tracks?market=GB&limit={limit}&offset={(i)*limit}",
                                                headers=get_auth_header(self.token))
                        playlist_dict=json.loads(my_playlist.content)

                        if playlist_dict['items']:
                                items.extend(playlist_dict['items'])                           
                trackArr=[]
                for track in items:
                        trackArr.append({"name":track['track']['name'],"artists":list(map(self.return_artists,track['track']['artists']))})
                return trackArr

        def get_current_user_id(self):
                response=requests.get("https://api.spotify.com/v1/me",headers=get_auth_header(self.token))
                response_json=json.loads(response.content)
                return response_json["id"]

        def get_users_playlists(self,users_id,limit=20,page_limit=1):
                page=0
                items=[]
                tick=0
                while True:
                        if tick==page_limit:
                                break
                        my_playlist= requests.get(f"https://api.spotify.com/v1/users/{users_id}/playlists?market=GB&limit={limit}&offset={page*limit}",
                                                headers=get_auth_header(self.token))
                        playlist_dict=json.loads(my_playlist.content)
                        tick+=1
                        if playlist_dict['items']:
                                items.extend(playlist_dict['items'])
                                page+=1
                        if not playlist_dict['items']:
                                break
                playlist_name_and_id=[]
                for playlist in items:
                        playlist_name_and_id.append({"name":playlist['name'],"id":playlist['id']})
                return playlist_name_and_id