"""Get Song Titles From Spotify Playlist

The following script uses the Spotify API to access song data from any playlist,
and dump the song titles and artist name in a text file to use as search requests in the
YouTube data API. The ID for any playlist can be found at the end of the URL for the playlist.

Functions: 

    * get_track_id - returns a list of unique track ID's from the playlist
    
    * get_track_data - returns a dictionary of the artists' names and song titles
    
    * main - driver code
"""

import json
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'c868d9b22a224b50a836141a713834c0'  # user id for spotify developer account
client_secret = 'f82b3b8855ad424a90ff6c49aa2ee4fb'  # private key for API access
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)  # send credentials to the server
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # sp will be the spotify API client
country_code = 'IE'  # needed for metadata 


# gets track ids from the playlist
def get_track_id(playlist_id): 
    id_list = []
    playlist = sp.playlist(playlist_id)  # get the playlist
    for i in playlist['tracks']['items']:  # access track info from json generated from playlist method
        track = i['track']  # get the track from the playlist
        id_list.append(track['id'])  # append only the track id
    return id_list


# get tracks metadata from the track id
def get_track_data(track_id):
    meta = sp.track(track_id, country_code)  # generates a json file with tracks metadata
    details = {
        'name': meta['name'], 
        'artist': meta['album']['artists'][0]['name']  # only getting song title and artist name
    }
    return details


def main():
    tracks = []  # to be filled with song title and artist name from get_track_data
    playlist_id = '4uxJSO6cN6i0HFD4FkDl9R'  # TODO: make playlist_id an input variable after testing
    track_id = get_track_id(playlist_id)
    for i in range(len(track_id)):
        time.sleep(.5)  # so as not to overload the server
        track = get_track_data(track_id[i])  # get the song title and artist name
        tracks.append(track['name'] + ' - ' + track['artist'] )  # append them to list
    print(tracks)  #testing
    try:
        # generate a text file of all the songs to use in the youtube data API
        with open('setup\searches.txt', 'w') as outfile:
            json.dump(tracks, outfile, indent=4)
            print("> Done.")
    except FileNotFoundError as e:
        print(e)
    
if __name__ == '__main__':
    main()
    