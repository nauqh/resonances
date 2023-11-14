from data.make_dataset import to_csv
from model.utils import get_token, get_features, get_artist
from pathlib import Path
from tqdm import tqdm
import pandas as pd

if __name__ == "__main__":
    # TODO: RAW JSON -> CSV SLIDE
    # base = Path('D:/Study/Monash/FIT3162/Resonance/data')
    # indir = base / 'raw'
    # outdir = base / 'processed'

    # to_csv(indir, outdir)

    # TODO: CSV SLIDE -> ARTISTS, FEATURES
    slide = pd.read_csv(
        "D:/Study/Monash/FIT3162/Resonance/data/processed/mpd.slice.0-999.json.csv")

    # Get tracks info as dataframe
    track_ids = slide['track_uri'].tolist()
    tracks = [get_features(get_token(), id) for id in tqdm(track_ids[:30])]
    track_df = pd.DataFrame(tracks)

    track_df.to_csv(
        "D:/Study/Monash/FIT3162/Resonance/data/combine/tracks/sampletrack.csv", index=False)

    # Get artists info as dataframe
    artist_ids = list(set(slide['artist_uri'].tolist()))
    artists = [get_artist(get_token(), id) for id in tqdm(artist_ids[:30])]
    artist_df = pd.DataFrame(artists)

    artist_df.to_csv(
        "D:/Study/Monash/FIT3162/Resonance/data/combine/artists/sampleartist.csv", index=False)
