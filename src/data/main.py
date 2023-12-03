from utils import get_token
from pathlib import Path
from make_dataset import raw_to_csv, csv_to_combine
from tqdm import tqdm
import os

if __name__ == "__main__":
    # TODO: RAW JSON -> CSV SLIDE
    base = Path(
        'D:/Study/Monash/FIT3162/Resonance/data/Million Playlist Dataset')
    raw = base / 'raw'
    processed = base / 'processed'
    combined = base / 'combined'

    raw_to_csv(raw, processed)

    # TODO: CSV SLIDE -> ARTISTS, TRACKS
    token = get_token()
    fnames = os.listdir(processed)

    for fname in tqdm(fnames):
        print(f"\nProcess slide {fname}")
        path = os.path.join(processed, fname)
        csv_to_combine(path, token)