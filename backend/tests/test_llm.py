import os
import langchain_core
import openai
import pydantic
from src.llm import LLM
from dotenv import load_dotenv, find_dotenv
import pytest
load_dotenv(find_dotenv())


def test_invalid_api_key():
    with pytest.raises(openai.AuthenticationError):
         LLM("my invalid api key").analyze("pop")

    with pytest.raises(pydantic.v1.error_wrappers.ValidationError):
         LLM("").analyze("pop")


def test_invalid_inputs():
    inputs = ["", "The idea is to loop through a list of letters", "Some activities require no more than the naked eye", "asodifhureiog lkaeurgheih"]
    for input in inputs:
        assert LLM(os.environ['API_KEY']).analyze(input) == None


def test_valid_inputs():
    inputs = ["pop music with a strong, energetic beat", "genre similar to artists like The Beatles and AC/DC"]
    genres = ["pop", "rock"]

    for i in range(len(inputs)):
        analysis = LLM(os.environ['API_KEY']).analyze(inputs[i])
        assert analysis != None
        assert "genre" in analysis
        assert genres[i] in analysis['genre'].lower()
        assert "mood" in analysis
        assert "color" in analysis
        assert "characteristics" in analysis
        assert len(analysis["characteristics"]) == 2
        assert "artists" in analysis
        assert len(analysis["artists"]) == 2
        assert "content" in analysis
        assert len(analysis["content"]) == 2

        
