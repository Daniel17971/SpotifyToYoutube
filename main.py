from spotify_request_tracks import get_tracks_and_artists
from auth_code import get_token

token=get_token()

tracks_artists_arr=get_tracks_and_artists(token,10)

print(tracks_artists_arr)