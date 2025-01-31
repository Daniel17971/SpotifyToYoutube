from json import JSONDecodeError
import requests
import os
BASE_URL= os.getenv("ID_CONVERSION_API_URI")


class IdConversionRequests:
    def __init__(self):
        self.BASE_URL = BASE_URL

    def check_song_exists(self, spotify_id):
        """check a song exists by its spotify Id."""
        response = requests.get(f"{BASE_URL}/songs/spotify_id/{spotify_id}")

        if response.status_code != 200:
            print(f"Failed to patch song status code: {response.status_code}, Response: {response.text}")
            return False
        
        try:
            return [True,response.json()]
        
        except JSONDecodeError:
            print(f"Failed to decode response: {response.text}")
            return False

    def check_song_has_youtube_id(self, spotify_id):
        """Check a songs has a youtube Id"""
        response = requests.get(f"{BASE_URL}/songs/spotify_id/{spotify_id}")

        if response.status_code != 200:
            print(f"Failed to patch song status code: {response.status_code}, Response: {response.text}")
            return False
        
        try:
            data = response.json()
            if data.get("youtube_id"):
                return True
            else: 
                return False
        
        except JSONDecodeError:
            print(f"Failed to decode response: {response.text}")
            return False

    def post_spotify_song(self, body):
        """Add a new spotify song and ID to the database."""
        response = requests.post(f"{BASE_URL}/songs", json=body)
        
        if response.status_code != 201:
            print(f"Failed to post song status code: {response.status_code}, Response: {response.text}")
            return None
        
        try:
            return response.json()
        
        except JSONDecodeError:
            print(f"Failed to decode response: {response.text}")
            return None

    def patch_existing_with_youtube_id(self,spotify_id,body):
        """Add a new youtube ID to a existing song in the database."""
        response = requests.patch(f"{BASE_URL}/songs/spotify_id/spotify_id/{spotify_id}", json=body)

        if response.status_code != 200:
            print(f"Failed to patch song status code: {response.status_code}, Response: {response.text}")
            return None
        
        try:
            return response.json()
        
        except JSONDecodeError:
            print(f"Failed to decode response: {response.text}")
            return None

