import json
import requests

BASE = "http://127.0.0.1:8000/"


# Get analysis
description = input("What kind of music do you like to listen to: ")
analysis = requests.post(
    BASE + 'analysis',
    json={"description": description}).json()

# Get artist info and add 'content' key for each artist
analysis['artists'] = [
    {**artist, 'content': content}
    for artist, content in zip(
        requests.post(BASE + 'artist',
                      json={"names": analysis['artists']}).json(),
        analysis['content'])
]
del analysis['content']

# Get song recommendation
ids = [artist['id'] for artist in analysis['artists']]

songs = requests.post(BASE + "recommendation",
                      json={"ids": ['57okaLdCtv3nVBSn5otJkp', '5HenzRvMtSrgtvU16XAoby']}).json()

analysis['tracks'] = [song['id'] for song in songs]


with open("data.json", "w") as f:
    json.dump(analysis, f)
