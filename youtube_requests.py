import os
import requests
import json



def search_videos(key,query_string):
    response=requests.get(f"https://www.googleapis.com/youtube/v3/search",params={
        'key': key,
        'q': query_string,
        'type': 'video',
        'part': 'snippet'
    })
    response_json=json.loads(response.content)
    videoArr=[]
    for item in response_json['items']:
        videoArr.append({'kind':item['id']['kind'],'videoId':item['id']['videoId'],'title':item['snippet']['title']})
    return videoArr

def create_playlist(playlist_name, token):
    response=requests.post(f"https://www.googleapis.com/youtube/v3/playlists",params={
        'part': 'snippet'
    },json={
        'snippet':{
            'title':playlist_name
        }
    },headers={"Authorization": "Bearer " + token})
    response_json=json.loads(response.content)
    return response_json['id']

def update_playlist(playlist_id, video_id, token):
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
    response_json=json.loads(response.content)
    return response_json

def get_youtube_key():
    return os.getenv("GOOGLE_API_KEY") 
