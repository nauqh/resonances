from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
# run python3 -m backend.app.main once pydantic is setup properly
#from ..src.utils import utils

app = FastAPI(title='Resonance', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "Root endpoint"}

@app.get("/example/{example_name}")     # example json api call, will find the json file (currently in the same dir, may change later)
def example(example_name):
    with open(f'{example_name}.json') as ex:
        ex_j = json.load(ex)
    ex.close()
    return ex_j

@app.get("/generate/{spotify_account}")
def generate_taste(spotify_account):
    #todo call individual data jsons, pass spotify account into the ones that need them
    return {"test", spotify_account}

# build individual data jsons, use utils for playlists and artists from spotify api
def get_artists():
    return {"artists"}

def get_tracks():
    return {"tracks"}

def get_playlists():
    return {"playlists"}

"""
cd backend
uvicorn app.main:app --reload
"""
