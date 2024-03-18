from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

class Example(BaseModel):
    genre: str

@app.get("/")
def root():
    return {"message": "Root endpoint"}

@app.get("/example/")     # example json api call, will find the json file 
def example(example_name: Example):
    genre = example_name.genre
    print(example_name)
    with open(f'examples/{genre}.json') as ex:
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