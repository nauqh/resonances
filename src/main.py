from data.make_dataset import to_csv
from requests import get
from model.utils import get_token, get_header, get_features, get_artist
from pathlib import Path
from tqdm import tqdm
import pandas as pd


def get_track(token: str, id: str) -> pd.DataFrame:
    url = f"https://api.spotify.com/v1/tracks/{id}"
    headers = get_header(token)
    track = get(url, headers=headers).json()

    artist = track['artists'][0]['id']
    features = get_features(token, id)

    return pd.DataFrame([{
        'id': id,
        'name': track['name'],
        'images': track['album']['images'],
        'release_date': track['album']['release_date'],
        'url': track['external_urls']['spotify'],
        'artist': artist,
        'popularity': track['popularity'],
        **features
    }])


def process_slide(slide: pd.DataFrame, token: str, outdir: Path) -> None:
    """
    Process a slide into artists and tracks dataframe
    """
    # Get tracks info as dataframe
    track_ids = slide['track_uri'].tolist()
    data = [get_track(token, id) for id in tqdm(track_ids[:10])]

    pd.concat(data, ignore_index=True).to_csv(
        outdir / 'combine/tracks.csv', index=False)

    # Get artists info as dataframe
    artist_ids = slide['artist_uri'].unique()[:10]
    artists = [get_artist(token, artist_id)
               for artist_id in tqdm(artist_ids)]

    pd.DataFrame(artists).to_csv(
        outdir / 'combine/artists.csv', index=False)


if __name__ == "__main__":
    # TODO: RAW JSON -> CSV SLIDE
    base = Path('D:/Study/Monash/FIT3162/Resonance/data')
    indir = base / 'raw'
    outdir = base / 'processed'

    to_csv(indir, outdir)

    # TODO: CSV SLIDE -> ARTISTS, FEATURES
    slide = pd.read_csv(
        "D:/Study/Monash/FIT3162/Resonance/data/processed/mpd.slice.0-999.json.csv")
    token = get_token()

    process_slide(slide, token, base)
