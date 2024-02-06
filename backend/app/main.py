from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from src.utils import search_artist, get_playlist, get_recommendation
from ..src.llm import LLM
import os

app = FastAPI(title='Resonance', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


@app.get("/")
def root():
    return {"message": "Root endpoint"}


@app.post("/analysis", status_code=status.HTTP_201_CREATED)
def create_analysis(description: dict):
    return LLM(os.environ['API_KEY']).analyze(description)


@app.post("/playlist", status_code=status.HTTP_201_CREATED)
def create_playlist(keyword: dict):
    return get_playlist(keyword)


@app.post("/artist", status_code=status.HTTP_201_CREATED)
def create_artist(data: dict):
    artists = []

    for name in data['names']:
        resp = search_artist(name)
        artist = {
            "name": name,
            "img": resp['items'][0]['images'][1]['url'] or resp['items'][0]['images']['url'],
            "id": resp['items'][0]['id']}
        artists.append(artist)
    return artists


@app.post("/recommendation", status_code=status.HTTP_201_CREATED)
def create_recommendation(data: dict):
    rec = get_recommendation(data['ids'])

    result_list = [{'id': track['id'],
                    'name': track['name']} for track in rec['tracks']]
    return result_list
