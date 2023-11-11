import base64
from tqdm import tqdm
import pandas as pd
from requests import post, get

client_id = ""
client_secret = ""


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


def extract_playlist(token: str, url: str) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    playlist = get_playlist(token, url)

    # Get tracks info as dataframe
    features = []

    for track in tqdm((playlist['tracks']['items'])):
        id = track['track']['id']
        features.append(get_features(token, id))

    feature_df = pd.DataFrame(features)

    # Get artists info as dataframe
    artist_ids = {track['track']['artists'][0]['id']
                  for track in playlist['tracks']['items']}
    artists = [get_artist(token, id) for id in tqdm(artist_ids)]
    artist_df = pd.DataFrame(artists)

    return playlist, artist_df, feature_df


if __name__ == "__main__":
    token = get_token()
    playlist_url = 'https://open.spotify.com/playlist/4mih0AxheCVcIQaIMf1YAK?si=345baf5504f14e24'

    playlist, artists, features = extract_playlist(token, playlist_url)
    artists.to_csv('artists.csv', index=False)
    features.to_csv('features.csv', index=False)
