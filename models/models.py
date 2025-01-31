from flask import session, redirect

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
    <li><a href="/playlist/list">List of playlists available for transfer</a></li>
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
    {"".join([f"<a href={playlist['id']}?name={'_'.join(playlist['name'].split())} ><li>{playlist['name']}</li></a>" for playlist in playlists])}
    </ul>
    <a href="/">return to home</a>
    </div>"""

def transfer_playlist_service(playlistId,name):
    #redirect if not logged in
    if 'googleCredentials' not in session:
        return redirect('login')
    conversion=SearchArrayLogic(session['spotifyCredentials']["access_token"])
    #get video Ids from spotify and return youtube equivalent
    video_ids_arr=conversion.spotify_to_youtube_ids(playlistId,10,1)
    #create a playlist on youtube
    YT=YoutubeRequests()
    playlist_id=YT.create_playlist(name,session['googleCredentials']['token'])
    session['playlist_id']=playlist_id
    

    #update the new playlist with the video Ids

    result=conversion.update_playlist_with_youtube_ids(video_ids_arr,playlist_id,session['googleCredentials']['token'])

    if not result:
        return f"""<div>
        <p>FAILED to update playlist correctly.</p>
        <p>Part of the playlist may have been created.</p>
        <a href="https://www.youtube.com/feed/playlists">see youtube playlists</a>
        <a href="/">return to home</a>
                </div>"""


    return f"""<div>
    <h3>created a playlist</h3>
    <a href="https://www.youtube.com/feed/playlists">see youtube playlists</a>
    <a href="/">return to home</a>
    </div>"""