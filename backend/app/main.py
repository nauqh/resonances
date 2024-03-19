from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
# run python3 -m backend.app.main once pydantic is setup properly
from src.utils.utils import *
from src.llm import LLM

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
    return {'message': 'Root endpoint'}

@app.get("/analysis/")
def analyse(desc: dict):
    '''analysis endpoint calls LLM prompt gen'''
    return LLM(os.environ['OPENAI_KEY']).analyze(desc)

@app.get("/example/")
def example(example_name: dict):
    '''example endpoint from premade json'''
    genre = example_name['genre']
    with open(f'examples/{genre}.json') as ex:
        ex_j = json.load(ex)
    ex.close()
    return ex_j

@app.get("/artist_img_url/")
def get_artist_image(artist: dict):
    return {'url': search_artist(artist['artist'])['items'][0]['images'][0]['url']}    # scuffed as shit

def get_playlists():
    return {"playlists"}

def get_tracks():
    return {"tracks"}

# @app.get("/generate/{spotify_account}")
# def generate_taste(spotify_account):
#     #todo call individual data jsons, pass spotify account into the ones that need them
#     return {"test", spotify_account}

# build individual data jsons, use utils for playlists and artists from spotify api

# def parse_analysis(desc: dict):
#     '''parse analysis to get image url from spotify api of suggested artist'''
#     analysis = LLM(os.environ['OPENAI_KEY']).analyze(desc)
#     artists = analysis['artists']
#     images = {}

#     for artist in artists:
#         images[artist] = search_artist(artist)['images'][0]['url']    # stuffed up but whatever

#     return analysis, images

# class Analysis():
#     def __init__(self, desc) -> None:
#         self.analysis = LLM(os.environ['OPENAI_KEY']).analyze(desc)


"""
cd backend
uvicorn app.main:app --reload
"""