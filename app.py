import os
from flask import Flask, session, redirect, url_for
from models.authentication import google_callback, google_login, spotify_callback, spotify_login
from models.models import index_service, list_spotify_playlists_service, transfer_playlist_service


API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
FLASK_API_KEY= os.getenv("FLASK_API_KEY")
app = Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = FLASK_API_KEY
AUTH_URL='https://accounts.google.com/o/oauth2/auth'

#User pages

@app.route('/')
def index():
  return index_service()

@app.route('/playlist/list')
def list_spotify_playlist():
  return list_spotify_playlists_service()


@app.route('/playlist')
def playlist():
  return transfer_playlist_service()

# Login and auth with google and spotify

@app.route('/login')
def login():
  return google_login()

@app.route('/spotifyLogin')
def spotifyLogin():
  return spotify_login()

@app.route('/spotifycallback')
def spotifyCallback():
  return spotify_callback()

@app.route('/oauth2callback')
def oauth2callback():
   return google_callback()

@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('localhost', 8080, debug=True)