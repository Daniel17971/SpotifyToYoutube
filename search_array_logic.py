from youtube_requests import YoutubeRequests
from spotify_requests import SpotifyRequests




class SearchArrayLogic:

    def __init__(self, spotify_token):
        self.spotify_token=spotify_token
        self.SR=SpotifyRequests(self.spotify_token)
        self.YT=YoutubeRequests()

    def spotify_to_youtube_ids(self,playlistId,limit, page_limit=1):
        youtube_search_arr=[]
        
        tracks_and_artists_arr=self.SR.get_tracks_and_artists(playlistId,limit,page_limit)
        

        
        for track in tracks_and_artists_arr:
            query_string=track['name'] + " " + track['artists'][0]
            result=self.YT.search_videos(self.YT.key,query_string)
            if not result:
                return result
            youtube_search_arr.append(result[0]['videoId'])
            

        return youtube_search_arr


    def update_playlist_with_youtube_ids(self,id_arr, playlist_id, token):
        if not id_arr:
            return None
        for video_id in id_arr:
            self.YT.update_playlist(playlist_id, video_id, token)
        return None

