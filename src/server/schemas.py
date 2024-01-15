from pydantic import BaseModel


class Artist(BaseModel):
    name: str
