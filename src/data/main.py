from utils import get_token
from pathlib import Path
from make_dataset import raw_to_csv, process_slide
import pandas as pd

if __name__ == "__main__":
    # TODO: RAW JSON -> CSV SLIDE
    base = Path('D:/Study/Monash/FIT3162/Resonance/data')
    indir = base / 'raw'
    outdir = base / 'processed'

    raw_to_csv(indir, outdir)

    # TODO: CSV SLIDE -> ARTISTS, FEATURES
    slide = pd.read_csv(
        "D:/Study/Monash/FIT3162/Resonance/data/processed/mpd.slice.0-999.json.csv")
    token = get_token()

    process_slide(slide, token, base)
