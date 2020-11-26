import requests
import base64, json 
from secrets import *


#curl -X "POST" -H "Authorization: Basic ZjM4ZjAw...WY0MzE=" -d grant_type=client_credentials https://accounts.spotify.com/api/token

authUrl = "https://accounts.spotify.com/api/token"

authHeader = {}
authData = {}

def getAccessToken(clientID, clientSecret):
    #client id and client secret
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')


    authHeader['Authorization'] = 'Basic ' + base64_message
    authData['grant_type'] = "client_credentials"

    #res is respinse object
    res = requests.post(authUrl, headers = authHeader, data = authData)

    #turn response into json
    responseObject = res.json()
    #print(json.dumps(responseObject, indent=2))

    accessToken = responseObject['access_token']
    return accessToken

def getPlaylistTracks(token, playlistID):
    #get endpoint
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}"
    getHeader = {
        "Authorization": "Bearer "+token
    }
    res = requests.get(playlistEndPoint, headers = getHeader)
    playlistObject = res.json()
    return playlistObject


#now have acecess token (API Requests)
token = getAccessToken(clientID, clientSecret)
#playlistID = "4ZGv0hnVBb1t9KpzwC13BG?si=QkILxjuzTuWTxny__y7bug"
#this function gets the playlist ID 
def getPlaylistID(playlistURL):
        for index, letter in enumerate(playlistURL):
            if letter == 't' and playlistURL[index+1] == '/':
                return playlistURL[index+2::]

#enter first playlist URL
playlistID = getPlaylistID(input('Enter the first Playlist URL: '))
tracklist = getPlaylistTracks(token, playlistID)


# #this dumps data into json
# with open('tracklist.json','w') as f:
#     json.dump(tracklist, f)

#uncomment this later
# for t in tracklist['tracks']['items']:
#     songName = t['track']['name']
#     artistName = t['track']['artists'][0]['name']
#     print(artistName, "=", songName)

#enter first playlist URL
playlistID2 = getPlaylistID(input('Enter the second Playlist URL: '))
tracklist2 = getPlaylistTracks(token, playlistID2)

for t in tracklist['tracks']['items']:
    songName = t['track']['name']
    artistName = t['track']['artists'][0]['name']
    if songName in [tt['track']['name'] for tt in tracklist2['tracks']['items']]:
         print(artistName, ':', songName)




