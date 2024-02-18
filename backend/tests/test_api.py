import requests

BASE = "http://127.0.0.1:8000/"


def test_get_analysis():
    response = requests.post(BASE + 'analysis',
                             json={"description": "Korean Soft Indie"})
    assert response.status_code == 200

    analysis = response.json()
    assert len(analysis.keys()) == 6


def test_get_artist_info():
    response = requests.post(BASE + 'artist',
                             json={"names": ['Justin Bieber', 'Charlie Puth']})
    assert response.status_code == 200

    artists = response.json()
    assert len(artists) == 2


def test_get_recommendation():
    response = requests.post(BASE + "recommendation",
                             json={"ids": ['57okaLdCtv3nVBSn5otJkp', '5HenzRvMtSrgtvU16XAoby']})
    assert response.status_code == 200

    songs = response.json()
    assert len(songs) == 8


def test_get_playlist():
    ...


# Get artist info and add 'content' key for each artist
# analysis['artists'] = [
#     {**artist, 'content': content}
#     for artist, content in zip(
#         requests.post(BASE + 'artist',
#                       json={"names": analysis['artists']}).json(),
#         analysis['content'])
# ]
# del analysis['content']
