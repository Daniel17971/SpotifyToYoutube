from urllib.parse import urlencode
import webbrowser
import os
from dotenv import load_dotenv
load_dotenv()
client_id=os.getenv('CLIENT_SECRET')
client_secret=os.getenv('CLIENT_ID')

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))