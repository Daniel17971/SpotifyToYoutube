from youtube_requests import YoutubeRequests
from spotify_requests import SpotifyRequests
from id_conversion_requests import IdConversionRequests



class SearchArrayLogic:

    def __init__(self, spotify_token):
        self.spotify_token=spotify_token
        self.SR=SpotifyRequests(self.spotify_token)
        self.YT=YoutubeRequests()
        self.ID=IdConversionRequests()

    def spotify_to_youtube_ids(self,playlistId,limit, page_limit=1):
        youtube_search_arr=[]
        
        tracks_and_artists_arr=self.SR.get_tracks_and_artists(playlistId)
        
        #Check if spotify_id exists in database
        for track in tracks_and_artists_arr:
            spotify_id=track['id']
            result=self.ID.check_song_exists(spotify_id)

            # Update DB if song does not exist
            if not result:
                body={"spotify_id":spotify_id, "name": track['name'] + " " + track['artists'][0]}
                self.ID.post_spotify_song(body)

            youtube_id=self.ID.check_song_has_youtube_id(spotify_id)

            # if youtube_id exists add ID to arr
            if youtube_id[0]:
                youtube_search_arr.append(youtube_id[1]['youtube_id'])
    
            # Otherwise search youtube for the song and update DB accordingly
            else:
                query_string=track['name'] + " " + track['artists'][0]
                result=self.YT.search_videos(self.YT.key,query_string)
                if not result:
                    return result
                youtube_search_arr.append(result[0]['videoId'])
                self.ID.patch_existing_with_youtube_id(spotify_id,{"youtube_id":result[0]['videoId']})
        
        return youtube_search_arr


    def update_playlist_with_youtube_ids(self,id_arr, playlist_id, token):
        if not id_arr:
            return None
        for video_id in id_arr:
            self.YT.update_playlist(playlist_id, video_id, token)
        return True

