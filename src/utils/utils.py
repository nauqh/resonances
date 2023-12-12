import base64
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame
from requests import post, get
from config import settings

client_id = settings.ID
client_secret = settings.SECRET


def get_token() -> str:
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    resp = post(url, headers=headers, data=data).json()
    token = resp["access_token"]

    return token


def get_header(token: str):
    return {"Authorization": "Bearer " + token}


# TODO: EXTRACT
def get_playlist(token: str, playlist_url: str) -> dict:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_header(token)

    resp = get(url, headers=headers).json()
    return resp


def get_artist(token: str, artist_id: str) -> dict:
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_header(token)
    return get(url, headers=headers).json()


def get_features(token: str, track_id: str) -> dict:
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_header(token)
    return get(url, headers=headers).json()


def extract_tracks(playlist) -> DataFrame:
    tracks = []
    for track in tqdm(playlist['tracks']['items']):
        id, name, images, added_date, release_date, url, popularity = (
            track['track']['id'],
            track['track']['name'],
            track['track']['album']['images'],
            track['added_at'],
            track['track']['album']['release_date'],
            track['track']['external_urls']['spotify'],
            track['track']['popularity']
        )
        artist = track['track']['artists'][0]['id']
        features = get_features(token, id)

        tracks.append({
            'id': id,
            'name': name,
            'images': images,
            'added_date': added_date,
            'release_date': release_date,
            'url': url,
            'artist': artist,
            'popularity': popularity,
            **features
        })
    return pd.DataFrame(tracks)


def extract_artists(df) -> DataFrame:
    ids = {row['artist'] for _, row in df.iterrows()}
    artists = [get_artist(token, id) for id in tqdm(ids)]
    return pd.DataFrame(artists)


if __name__ == "__main__":
    token = get_token()

    tophits = [
        'https://open.spotify.com/playlist/37i9dQZF1DWUZv12GM5cFk?si=dfe480ed63ef4563',
        'https://open.spotify.com/playlist/37i9dQZF1DX9Ol4tZWPH6V?si=1ccf4ad83b514b57',
        'https://open.spotify.com/playlist/37i9dQZF1DX0P7PzzKwEKl?si=820bf3f0814441cd',
        'https://open.spotify.com/playlist/37i9dQZF1DXaW8fzPh9b08?si=f59ad4f829a14fba',
        'https://open.spotify.com/playlist/37i9dQZF1DWTWdbR13PQYH?si=cc95918ad7a44e82',
        'https://open.spotify.com/playlist/37i9dQZF1DWWzQTBs5BHX9?si=b7d8d71b97c846f5',
        'https://open.spotify.com/playlist/37i9dQZF1DX1vSJnMeoy3V?si=9f5b23f73e9845a9',
        'https://open.spotify.com/playlist/37i9dQZF1DX3j9EYdzv2N9?si=6f48e7df732e47f0',
        'https://open.spotify.com/playlist/37i9dQZF1DWYuGZUE4XQXm?si=4d2f17ed4b5547e4',
        'https://open.spotify.com/playlist/37i9dQZF1DX4UkKv8ED8jp?si=f6d57a06b3dd4692',
        'https://open.spotify.com/playlist/37i9dQZF1DXc6IFF23C9jj?si=de4369307bc249dc',
        'https://open.spotify.com/playlist/37i9dQZF1DXcagnSNtrGuJ?si=8e2de10460714279',
        'https://open.spotify.com/playlist/37i9dQZF1DX0yEZaMOXna3?si=687e6d67bb9f48c1',
        'https://open.spotify.com/playlist/37i9dQZF1DX3Sp0P28SIer?si=261304fcbda44b98',
        'https://open.spotify.com/playlist/37i9dQZF1DX0h0QnLkMBl4?si=16f306273d714cbb',
        'https://open.spotify.com/playlist/37i9dQZF1DX9ukdrXQLJGZ?si=4f6259ae085d4de8',
        'https://open.spotify.com/playlist/37i9dQZF1DX8XZ6AUo9R4R?si=c38ddde850b64443',
        'https://open.spotify.com/playlist/37i9dQZF1DWTE7dVUebpUW?si=c6407eb9911a4de3',
        'https://open.spotify.com/playlist/37i9dQZF1DXe2bobNYDtW8?si=19240e75a8634d5c',
        'https://open.spotify.com/playlist/37i9dQZF1DWVRSukIED0e9?si=5a5b0ebaf1f04358',
        'https://open.spotify.com/playlist/2fmTTbBkXi8pewbUvG3CeZ?si=4c4fdee325a94d8e',
        'https://open.spotify.com/playlist/5GhQiRkGuqzpWZSE7OU4Se?si=7fa9845ed9334a95',
        'https://open.spotify.com/playlist/56r5qRUv3jSxADdmBkhcz7?si=2ed1488f90d44f2c',
        'https://open.spotify.com/playlist/4hMcqod7ERKJ9mtjgdimeV?si=623987b5c6764164'
    ]

    for year, url in zip(range(2000, 2024), tophits):
        playlist = get_playlist(token, url)
        tracks = extract_tracks(playlist)
        artists = extract_artists(tracks)
        artists.to_csv(f'Spotify/artist/{year}_artists.csv', index=False)
        tracks.to_csv(f'Spotify/track/{year}_tracks.csv', index=False)
