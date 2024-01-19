from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import track, artist, analysis

app = FastAPI(title='Resonance', version='2.0.0')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(track.router)
app.include_router(artist.router)
app.include_router(analysis.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
