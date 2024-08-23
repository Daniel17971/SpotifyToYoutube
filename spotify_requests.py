import requests
from auth_code import get_auth_header
import json


def return_artists(arr):
                return arr['name']

def get_tracks_and_artists(token,limit):
        my_playlist= requests.get(f"https://api.spotify.com/v1/playlists/3MCN79RFWj2MKwcPC3K3ZB/tracks?market=GB&limit={limit}",
                                headers=get_auth_header(token))
        playlist_dict=json.loads(my_playlist.content)
        trackArr=[]

        for track in playlist_dict['items']:
                trackArr.append({"name":track['track']['name'],"artists":list(map(return_artists,track['track']['artists']))})
        
        return trackArr
        