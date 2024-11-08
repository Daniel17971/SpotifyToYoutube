# -*- coding: utf-8 -*-
import urllib
from search_array_logic import spotify_to_youtube_ids, update_playlist_with_youtube_ids
import os
from flask import Flask, session, abort, redirect, request, url_for
import google_auth_oauthlib.flow
import os
from spotify_auth import get_access_token, spotify_auth_url
from youtube_requests import YoutubeRequests
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "google_secrets.json"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
FLASK_API_KEY= os.getenv("FLASK_API_KEY")
app = Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = FLASK_API_KEY
AUTH_URL='https://accounts.google.com/o/oauth2/auth'


@app.route('/')
def index():
  if 'credentials' not in session:
    return redirect('login')
  if 'spotifyCredentials' not in session:
    return redirect('spotifyLogin')
  return f"""<div>
  <h3>welcome to spotify youtube sync</h3>
  <a href="/playlist">create a playlist</a>
  <a href="/logout">logout</a>
  </div>"""

@app.route('/playlist')
def playlist():
  #redirect if not logged in
  if 'credentials' not in session:
    return redirect('login')
  #get video Ids from spotify and return youtube equivalent
  video_ids_arr=spotify_to_youtube_ids(100,10)
  
  #create a playlist on youtube
  YT=YoutubeRequests()
  playlist_id=YT.create_playlist("Imperial Log 109",session['credentials']['token'])
  session['playlist_id']=playlist_id
  

  #update the new playlist with the video Ids

  result=update_playlist_with_youtube_ids(video_ids_arr,playlist_id,session['credentials']['token'])

  if not result:
    return f"""<div><p>failed to update playlist</p>
    <a href="/">return to home</a>
              </div>"""


  return f"""<div>
  <h3>created a playlist</h3>
  <a href="/">return to home</a>
  </div>"""

@app.route('/login')
def login():
  # google auth flow
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = url_for('oauth2callback', _external=True)
  authorization_url, state = flow.authorization_url(
      access_type='offline',
      prompt='select_account')
  session['state'] = state

  return redirect(authorization_url)

@app.route('/spotifyLogin')
def spotifyLogin():
  auth_request_params=spotify_auth_url()
  auth_url = "https://accounts.spotify.com/authorize/?" + urllib.parse.urlencode(auth_request_params)
  return redirect(auth_url)

@app.route('/spotifycallback')
def spotifyCallback():

  code = request.args.get('code')

  spotifyCredentials = get_access_token(authorization_code=code)

  session['spotifyCredentials'] = spotifyCredentials

  return redirect(url_for('index'))

@app.route('/oauth2callback')
def oauth2callback():
  if 'state' not in session:
    abort(400)
  
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)

  return redirect(url_for('index'))

@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('localhost', 8080, debug=True)