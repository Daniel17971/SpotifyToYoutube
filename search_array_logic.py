from youtube_requests import YoutubeRequests
from spotify_requests import SpotifyRequests


SR=SpotifyRequests()
YT=YoutubeRequests()

def spotify_to_youtube_ids(limit, page_limit=1):
    youtube_search_arr=[]
    
    tracks_and_artists_arr=SR.get_tracks_and_artists(limit,page_limit)
    

    
    for track in tracks_and_artists_arr:
        query_string=track['name'] + " " + track['artists'][0]
        result=YT.search_videos(YT.key,query_string)
        if not result:
            return result
        youtube_search_arr.append(result[0]['videoId'])
        

    return youtube_search_arr


def update_playlist_with_youtube_ids(id_arr, playlist_id, token):
    if not id_arr:
        return None
    for video_id in id_arr:
        YT.update_playlist(playlist_id, video_id, token)
    return None

