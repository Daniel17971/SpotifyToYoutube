from spotify_requests import get_tracks_and_artists
from spotify_auth import get_token
from youtube_requests import search_videos
import os
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API_KEY=os.getenv("GOOGLE_API_KEY")

def spotify_to_youtube_ids():
    youtube_search_arr=[]

    tracks_and_artists_arr=get_tracks_and_artists(get_token(),100)

    for track in tracks_and_artists_arr:
        query_string=track['name'] + " " + track['artists'][0]
        youtube_search_arr.append(search_videos(YOUTUBE_API_KEY,query_string)["items"][0]["id"]["videoId"])

    return youtube_search_arr

print(spotify_to_youtube_ids())



