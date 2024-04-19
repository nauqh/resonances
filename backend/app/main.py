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

@app.get("/")
def root():
    return {'message': 'Root endpoint'}

@app.post("/example/")
def example(example_name: dict):
    '''example endpoint from premade json'''
    genre = example_name['genre']
    with open(f'examples/{genre}.json') as ex:
        ex_j = json.load(ex)
    ex.close()
    return ex_j

@app.post("/analysis/")
def analyse(desc: dict):
    '''analysis endpoint calls LLM prompt gen'''
    return LLM(os.environ['OPENAI_KEY']).analyze(desc)

@app.post("/artist/")
def artist(artists: dict):
    res_list = []
    for artist in artists['names']:
        res_list.append({'name': artist,
                    'img': search_artist(artist)['items'][0]['images'][0]['url'],
                    'id': search_artist(artist)['items'][0]['id']})
    return res_list

@app.post("/playlist/")
def playlists(playlist: dict):
    return search_playlist(playlist['keyword'])

@app.post("/recommendation/")
def recommendation(recommendations: dict):
    return get_recommendation(recommendations['ids'])

"""
cd backend
uvicorn app.main:app --reload
"""