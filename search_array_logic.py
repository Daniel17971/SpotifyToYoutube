from spotify_requests import get_tracks_and_artists
from spotify_auth import get_token
from youtube_requests import search_videos, update_playlist
import os
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API_KEY=os.getenv("GOOGLE_API_KEY")

def spotify_to_youtube_ids(limit, page_limit=1):
    youtube_search_arr=[]

    tracks_and_artists_arr=get_tracks_and_artists(get_token(),limit,page_limit)


    
    for track in tracks_and_artists_arr:
        query_string=track['name'] + " " + track['artists'][0]
        youtube_search_arr.append(search_videos(YOUTUBE_API_KEY,query_string)[0]['videoId'])

    return youtube_search_arr


def update_playlist_with_youtube_ids(id_arr, playlist_id, token):
    for video_id in id_arr:
        update_playlist(playlist_id, video_id, token)
    return None