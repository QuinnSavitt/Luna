import webbrowser
from Module import Module
import requests
import Encoding
import datetime

# TODO: Cache all playlist links every week or on command?
access = ""
refresh = ""
last_refresh = datetime.datetime.now()


def Auth():
    global access
    global refresh
    client_id = '1ccf8f739640468ba412596fb04ef5bb'
    client_secret = ''
    redirect = "https://github.com/capitjeff21/Portfolio"
    # Use refresh token to not log in every time. TODO: save refresh token
    if refresh:
        response = requests.post('https://accounts.spotify.com/api/token',
                                 headers={'Content-Type': 'application/x-www-form-urlencoded',
                                          'Authorization': 'Basic ' + Encoding.encode64(
                                              client_id + ":" + client_secret)},
                                 data={'grant_type': 'refresh_token',
                                       'refresh_token': refresh})
        print(response.status_code)
        if response.status_code == 200:
            j = response.json()
            print(j)
            #refresh = j['refresh_token']
            access = j['access_token']
            f = open("SpotifyAccess.qrs", "w")
            #f.write(refresh)
            f.close()
            return

    r = requests.get('https://accounts.spotify.com/authorize?', data={'client_id': client_id,
                                                                      "response_type": 'code',
                                                                      'redirect_uri': redirect,
                                                                      'scope': 'user-read-private user-read-email user-modify-playback-state'})
    webbrowser.open(
        f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect}&scope=user-read-private user-read-email user-modify-playback-state')
    code = str(input("Please input the auth code you received"))
    response = requests.post("https://accounts.spotify.com/api/token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': 'Basic ' + Encoding.encode64(client_id + ":" + client_secret)},
                             data={'grant_type': 'authorization_code',
                                   'code': code,
                                   'redirect_uri': redirect})
    j = response.json()
    refresh = j['refresh_token']
    access = j['access_token']
    f = open("SpotifyAccess.qrs", "w")
    f.write(refresh)
    f.close()
    print(access)


class Spotify(Module):

    def __init__(self):
        global refresh
        super().__init__("spotify", ["play", "spotify", "music", "resume", "pause"])
        f = open("SpotifyAccess.qrs", "r")
        refresh = f.read()
        print(refresh)
        f.close()

    def process(self, text):
        if not access or (datetime.datetime.now() - last_refresh).total_seconds() > 3600:
            if refresh:
                Auth()
            else:
                return "please authenticate and try again", Auth
        print("processing")
        if " by " in text:
            text.replace(" by ", " ")
        if "the song" in text:
            response = requests.get('https://api.spotify.com/v1/search', headers={'Authorization': 'Bearer ' + access},
                                    params={'q': text[text.find("the song") + 8:].replace(" ", "+"),
                                            'type': 'track',
                                            'market': 'US',
                                            'limit': '1',
                                            'offset': '0'})
            j = response.json()
            id = j['tracks']['items'][0]["id"]
            name = j['tracks']['items'][0]['name']
            artist = j['tracks']['items'][0]['artists'][0]['name']
            return "now playing " + name + " by " + artist, lambda: self.playSong(id)

        if "the artist" in text:
            response = requests.get('https://api.spotify.com/v1/search', headers={'Authorization': 'Bearer ' + access},
                                    params={'q': text[text.find("the artist") + 10:].replace(" ", "+"),
                                            'type': 'artist',
                                            'market': 'US',
                                            'limit':'1',
                                            'offset': '0'})
            j = response.json()
            id = j['artists']['items'][0]['id']
            name = j['artists']['items'][0]['name']
            return f"now playing top songs by {name}", lambda: self.playArtist(id)
        if "the album" in text:
            response = requests.get('https://api.spotify.com/v1/search', headers={'Authorization': 'Bearer ' + access},
                                    params={'q': text[text.find("the song") + 8:].replace(" ", "+"),
                                            'type': 'track',
                                            'market': 'US',
                                            'limit': '1',
                                            'offset': '0'})
            j = response.json()
            uri = j['albums']['items'][0]["uri"]
            name = j['albums']['items'][0]['name']
            artist = j['albums']['items'][0]['artists'][0]['name']
            return "now playing " + name + " by " + artist, lambda: self.playAlbum(uri)
        if "the playlist" in text:
            pass

        if text in ["play", "resume"]:
            return "", self.resume

        if text in "pause":
            return "", self.pause

        else:
            return "please be more specific, ask for an artist, album, song, or playlist specifically"

    # Callbacks
    def playSong(self, songID):
        r = requests.put("https://api.spotify.com/v1/me/player/play", headers={'Authorization': "Bearer " + access,
                                                                               'Content-Type': 'application/json'},
                         data=f'{{"uris": ["spotify:track:{songID}"]}}')

    def playArtist(self, artistID):
        r = requests.put("https://api.spotify.com/v1/me/player/play", headers={'Authorization': "Bearer " + access,
                                                                               'Content-Type': 'application/json'},
                         data=f'{{"uris": ["spotify:artist:{artistID}"]}}')

    def playAlbum(self, uri):
        r = requests.put("https://api.spotify.com/v1/me/player/play", headers={'Authorization': "Bearer " + access,
                                                                               'Content-Type': 'application/json'},
                         data=f'{{"uris": ["{uri}"]}}')

    def resume(self):
        r = requests.put("https://api.spotify.com/v1/me/player/play", headers={'Authorization': "Bearer " + access,
                                                                               'Content-Type': 'application/json'})

    def pause(self):
        r = requests.put("https://api.spotify.com/v1/me/player/pause", headers={'Authorization': "Bearer " + access})
