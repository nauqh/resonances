from jsonschema import validate
from dotenv import load_dotenv
import json, os
load_dotenv()
path = os.environ['SCHEMA_PATH']

def open_file(filename):
    with open(filename) as f:
        out = json.load(f)
        f.close()
        return out

def validate_json(endpoint: dict, schema: str):
    validate(instance = endpoint, schema = open_file(f'{path}{schema}.json'))