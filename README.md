# Spotify-Playlist-Downloader
Program that makes use of the Spotify and YouTube Data API to download spotify playlists from YouTube MP3s.

Files:
get_spotify_titles.py:
Using the Spotify API, we input the playlist ID for any playlist (which can be found in the URL for the playlist) into the get_track_id() function.
This function puts the playlist ID into a method from the Spotify API called playlist() which returns a json file of the playlist data.
Then we loop on just the data from 'tracks' and append the IDs to a list. Then the track IDs get passed to the next function called get_track_data() which passes
the IDs to another method from the API called track() which generates a json for each individual track. Then we append just the song title and artist name
to a dictionary and return it. In the main() function is where we pass the playlist ID and then loop on each track ID and append the Song title and artist name
to a text file to be used in the make_playlist.py script.

make_playlist.py:
Using the YouTube Data API, we first get all the song titles and artist names from the searches.txt file and append them to a list. We then send each line of the 
searches file as a search query for the YouTube API. The results from the search query returns a json file with the Youtube video information. We take the video
ID and add it to the end of the YouTube watch link. Then, in the download() function, we use Pytube to download each video link, using audio_only=True to only download 
the MP3 of each video.
