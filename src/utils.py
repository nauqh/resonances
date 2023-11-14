import base64
from tqdm import tqdm
import pandas as pd
from requests import post, get

client_id = "41ebc65d020d4aa8be24bd1f97cbd9ed"
client_secret = "62ceb3db85854f739c3fd9598504ecaf"


def get_token():
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


def extract_tracks(playlist) -> pd.DataFrame:
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


def extract_artists(df) -> pd.DataFrame:
    ids = {row['artist'] for _, row in df.iterrows()}
    artists = [get_artist(token, id) for id in tqdm(ids)]
    return pd.DataFrame(artists)


if __name__ == "__main__":
    token = get_token()
    url = 'https://open.spotify.com/playlist/4mih0AxheCVcIQaIMf1YAK?si=345baf5504f14e24'

    playlist = get_playlist(token, url)
    tracks = extract_tracks(playlist)
    artists = extract_artists(tracks)
    artists.to_csv('artists.csv', index=False)
    tracks.to_csv('features.csv', index=False)
