from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import track

app = FastAPI(title='Resonance', version='2.0.0')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(track.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
