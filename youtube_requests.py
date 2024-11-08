import os
import requests
import json


class YoutubeRequests:

    def __init__(self):
        self.key=os.getenv("GOOGLE_API_KEY")
    
    def search_videos(self,key,query_string):
        response=requests.get(f"https://www.googleapis.com/youtube/v3/search",params={
            'key': key,
            'q': query_string,
            'type': 'video',
            'part': 'snippet'
        })
        response_json=json.loads(response.content)
        videoArr=[]
        if not response.ok:
            print(f"failed to return results, status code: {response.status_code} Response: {response.text}")
            return None
        for item in response_json['items']:
            videoArr.append({'kind':item['id']['kind'],'videoId':item['id']['videoId'],'title':item['snippet']['title']})
        return videoArr

    def create_playlist(self,playlist_name, token):
        response=requests.post(f"https://www.googleapis.com/youtube/v3/playlists",params={
            'part': 'snippet'
        },json={
            'snippet':{
                'title':playlist_name
            }
        },headers={"Authorization": "Bearer " + token})

        if response.status_code!=200:
            print(f"failed to create playlist, status code: {response.status_code} Response: {response.text}")
            return f"<p>failed to create playlist</p>"

        response_json=json.loads(response.content)
        return response_json['id']

    def update_playlist(self,playlist_id, video_id, token):
        response=requests.post(f"https://www.googleapis.com/youtube/v3/playlistItems",params={
            'part': 'snippet'
        },json={
            'snippet':{
                'playlistId':playlist_id,
                'resourceId':{
                    'kind':'youtube#video',
                    'videoId':video_id
                }
            }
        },headers={"Authorization": "Bearer " + token})
        if response.status_code!=200:
            print(f"failed to update playlist, status code: {response.status_code} Response: {response.text}")
            return f"<p>failed to update playlist</p>"
        response_json=json.loads(response.content)
        return response_json


