from flask import Flask, session, abort, redirect, request, url_for

from search_array_logic import SearchArrayLogic
from spotify_requests import SpotifyRequests
from youtube_requests import YoutubeRequests

def index_service():  
    if 'googleCredentials' not in session:
        return redirect('login')
    if 'spotifyCredentials' not in session:
        return redirect('spotifyLogin')
    return f"""<div>
    <h3>welcome to spotify youtube sync</h3>
    <p>Welcome, this website will covert one of your spotify playlist into a youtube playlist, please see the options below: </p>
    <ul>
    <li><a href="/playlist/list">show availiable spotify playlists</a></li>
    <li><a href="/playlist">transfer a playlist</a></li>
    <li><a href="/logout">logout</a></li>
    </ul>
    </div>"""

def list_spotify_playlists_service():
    #redirect if not logged in
    if 'googleCredentials' not in session:
        return redirect('login')
    #get user id from spotify
    SR=SpotifyRequests(session['spotifyCredentials']["access_token"])
    user_id=SR.get_current_user_id()
    #get user playlists from spotify
    playlists=SR.get_users_playlists(user_id)
    return f"""<div>
    <h3>playlists</h3>
    <ul>
    {"".join([f"<li>{playlist['name']}</li>" for playlist in playlists])}
    </ul>
    <a href="/">return to home</a>
    </div>"""

def transfer_playlist_service():
    #redirect if not logged in
    if 'googleCredentials' not in session:
        return redirect('login')
    conversion=SearchArrayLogic(session['spotifyCredentials']["access_token"])
    #get video Ids from spotify and return youtube equivalent
    video_ids_arr=conversion.spotify_to_youtube_ids(10,1)
    
    #create a playlist on youtube
    YT=YoutubeRequests()
    playlist_id=YT.create_playlist("Imperial Log 109",session['googleCredentials']['token'])
    session['playlist_id']=playlist_id
    

    #update the new playlist with the video Ids

    result=conversion.update_playlist_with_youtube_ids(video_ids_arr,playlist_id,session['googleCredentials']['token'])

    if not result:
        return f"""<div><p>failed to update playlist</p>
        <a href="/">return to home</a>
                </div>"""


    return f"""<div>
    <h3>created a playlist</h3>
    <a href="/">return to home</a>
    </div>"""