from flask import abort, redirect, request, session, url_for
import google_auth_oauthlib
import os

import urllib
from spotify_auth import get_access_token, spotify_auth_url

CLIENT_SECRETS_FILE = "google_secrets.json"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def google_login():
  # google auth flow
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = url_for('oauth2callback', _external=True)
  authorization_url, state = flow.authorization_url(
      access_type='offline',
      prompt='select_account')
  session['state'] = state

  return redirect(authorization_url)

def spotify_login():
  auth_request_params=spotify_auth_url()
  auth_url = "https://accounts.spotify.com/authorize/?" + urllib.parse.urlencode(auth_request_params)
  return redirect(auth_url)

def spotify_callback():

  code = request.args.get('code')

  spotifyCredentials = get_access_token(authorization_code=code)

  session['spotifyCredentials'] = spotifyCredentials

  return redirect(url_for('index'))

def google_callback():
  if 'state' not in session:
    abort(400)
  
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = url_for('oauth2callback', _external=True)

  authorization_response = request.url
  flow.fetch_token(authorization_response=authorization_response)

  credentials = flow.credentials
  session['googleCredentials'] = credentials_to_dict(credentials)

  return redirect(url_for('index'))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}