"""Download Spotify Playlist From YouTube

NOTE: API key can be found on the YouTube Data API page (found in docs/references.txt)

The following script uses the 'searches.txt' file generated in 'get_spotify_titles'
and sends each line as a request to YouTube's search engine via the YouTube Data API.
The request returns a JSON file of all the metadata from the YouTube video, including the 
video ID, which we then append on to the end of a YouTube URL template. With the list of links,
we pass that list to the download function, which filters only the MP3 files from the video
and saves them to the downlaods folder.

Functions:
    * get_search_titles - Adds each line from 'searches.txt' to a list and formats them for the search engine
    
    * establish_connection - Let's us know if the connection to the API is successful or not.
    
    * access_youtube_API - Creates a YouTube object for sending requests to the search engine, and gets the video ID
                           from the request result. This ID is appended to the YouTube link template.
                           
    * download - Takes the list of links and downloads them to SAVE_PATH.
"""

import requests 
import time
from datetime import timedelta
from requests.exceptions import HTTPError
from googleapiclient.discovery import build
from pytube import YouTube
import pytube
from pprint import PrettyPrinter

url = 'https://www.youtube.com'  # establish connection to youtube
API_KEY = input('Enter API key: ')  # key for accessing youtubes developer API
SAVE_PATH = input("Enter save path for playlist: ")  # path that the songs will download to
titles = []  # list of titles to search for
links = []  # list of links to download


# get titles from file
def get_search_titles(file):
    with open(file, newline='') as f:
        for line in f:
            if not len(line) < 5:  # make sure the titles are valid
                # remove the quotes and commas
                line = line.replace('"', '')
                line = line.replace(',', '') 
                titles.extend(line.strip().split(', '))  # append them to list removing whitespace
    print(titles)  # testing


# confirm successful connection to API
def establish_connection(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises HTTP error if connection fails
    except HTTPError as http_err:
        print(f'> HTTP error occurred: {http_err}')
    except Exception as e:
        print(f'> Unknown error occured: {e}')
    else:
        print('> Success')


# connect to API and send search requests
def access_youtube_API(key):
    global request
    youtube = build('youtube', 'v3', developerKey=key)  # create youtube object
    #print(type(youtube))  # testing
    for title in titles:
        request = youtube.search().list(
            q=title,  # q is the search query which here is each title in titles
            part='id',  # only interested in the video ID
            type='video',
            maxResults=1
        )
        time.sleep(1)  # to not overload the server
        try:
            res = request.execute()
            # pp = PrettyPrinter()
            # pp.pprint(res)  # testing
            for vid in res['items']:
                links.append(f"https://www.youtube.com/watch?v={vid['id']['videoId']}")  # append the video ID to the youtube URL
        except:
            print("API Error: daily request quota reached")


# download list of youtube links the SAVE_PATH
def download(list):
    for i in list:
        try:
            yt = YouTube(i)  # construct an object for each url
        except:
            print('error')
        song = yt.streams.filter(fps=None, only_audio=True)  # filter each video to only get the MP3
        mp3_file = pytube.Stream(song, monostate=list) # create a stream object to download
        try:
            mp3_file.download(SAVE_PATH)  # download each link to SAVE_PATH
        except Exception as ex:
            print(f"Error: {ex}")
    print("Done")


def main():
    start_time = time.time()
    get_search_titles('setup\searches.txt')   
    access_youtube_API(API_KEY) 
    print(links)
    download(links)
    execution_time = ((time.time() - start_time) / 60)
    if execution_time < 1:
        print('Execution time: < 1 min')
    else:
        print('Execution time: {:.2f} mins'.format(execution_time))


if __name__ == '__main__':
    main()
