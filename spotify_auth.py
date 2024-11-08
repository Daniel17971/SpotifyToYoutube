import base64
import uuid
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()

client_id=os.getenv('SPOTIFY_CLIENT_ID')
client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
scopes = "playlist-read-private"
redirect_uri= os.getenv('SPOTIFY_REDIRECT_URI')

def spotify_auth_url():
    auth_request_params={
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scopes,
        "show_dialog": "true",
        "state": str(uuid.uuid4())

    }
    return auth_request_params

def get_access_token(authorization_code:str):
    spotify_request_access_token_url = 'https://accounts.spotify.com/api/token/?'
    body = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id' : client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
        }
    response = requests.post(spotify_request_access_token_url, data = body)
    if response.status_code != 200:
        raise Exception ('Failed to obtain Access token')
    return response.json()


def get_token():
    auth_string=client_id+ ":" + client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")

    url="https://accounts.spotify.com/api/token"

    headers={
        "Authorization": "Basic" + " " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={"grant_type":"client_credentials"}
    result=requests.post(url, headers=headers,data=data)
    json_result=json.loads(result.content)
    return json_result["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

