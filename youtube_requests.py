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

