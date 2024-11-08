import requests
from spotify_auth import get_auth_header, get_token
import json


class SpotifyRequests:

        def __init__(self):
                self.token=get_token()

        def return_artists(self,arr):
                        return arr['name']

        def get_tracks_and_artists(self,limit,page_limit=1):
                page=0
                items=[]
                tick=0

                while True :
                        if tick==page_limit:
                                break
                        
                        my_playlist= requests.get(f"https://api.spotify.com/v1/playlists/3MCN79RFWj2MKwcPC3K3ZB/tracks?market=GB&limit={limit}&offset={page*limit}",
                                                headers=get_auth_header(self.token))
                        playlist_dict=json.loads(my_playlist.content)
                        tick+=1

                        if playlist_dict['items']:
                                items.extend(playlist_dict['items'])
                                page+=1
                                
                        if not playlist_dict['items']:
                                break
                trackArr=[]
                for track in items:
                        trackArr.append({"name":track['track']['name'],"artists":list(map(self.return_artists,track['track']['artists']))})
                
                return trackArr

