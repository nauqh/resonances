from utils import get_token
from pathlib import Path
from make_dataset import raw_to_csv, csv_to_combine
import pandas as pd
from tqdm import tqdm
import os

if __name__ == "__main__":
    # TODO: RAW JSON -> CSV SLIDE
    base = Path('D:/Study/Monash/FIT3162/Resonance/data')
    indir = base / 'raw'
    outdir = base / 'processed'

    # raw_to_csv(indir, outdir)

    # # TODO: CSV SLIDE -> ARTISTS, FEATURES
    token = get_token()
    fnames = os.listdir(outdir)

    for fname in tqdm(fnames):
        print(f"Process slide {fname}")
        slide = pd.read_csv(os.path.join(outdir, fname))
        csv_to_combine(slide, token, base)
