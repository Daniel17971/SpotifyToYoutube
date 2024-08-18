import requests
import os
from dotenv import load_dotenv

load_dotenv()

id=os.getenv('CLIENT_SECRET')
secret=os.getenv('CLIENT_ID')

data={'grant_type':'client_credentials',
        'client_id':f'{id}',
        'client_secret':f'{secret}'
        }

my_playlist= requests.get("https://api.spotify.com/v1/playlists/3MCN79RFWj2MKwcPC3K3ZB?market=GB",
                           headers={'Authorization':'Bearer  BQBnHbQkqcF5cBiVA2qj-_ypCqktriiHxL4FmNDFU1GLWUtdObn9MsRN06EZyQumGj_zy4f8RPQ2JAHo0Oz90H9HthrUalYEwPiXSDts9kfA1n0ngqs'})

print(my_playlist.content)
