import requests
import pandas as pd
import json

BASE = "http://127.0.0.1:8000/"


def test_artists():
    URL = BASE + "artists"

    resp = requests.post(
        URL, json={"names": ['Justin Bieber', 'Imagine Dragons']})
    imgs = resp.json()
