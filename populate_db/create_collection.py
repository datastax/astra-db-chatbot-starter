'''
import json
import requests

import sys

sys.path.append('utils')
from local_creds import *

url = f"https://{ASTRA_DB_ID}-{ASTRA_DB_REGION}.apps.astra.datastax.com/api/json/v1/{ASTRA_DB_NAMESPACE}"
print(url)

payload = json.dumps({"createCollection": {
    "name": "chat",
    "options" : {
        "vector" : {
            "size" : 1536,
            "function" : "cosine"}}}})

headers = {
    'x-cassandra-token': ASTRA_DB_APPLICATION_TOKEN,
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
'''
import os

from dotenv import load_dotenv

from astrapy.db import AstraDB

load_dotenv()

# Grab the Astra token and api endpoint from the environment
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
keyspace = os.getenv("ASTRA_DB_KEYSPACE")
collection_name = os.getenv("ASTRA_DB_COLLECTION_NAME")
dimension = os.getenv("VECTOR_DIMENSION")

if not keyspace:
    keyspace = "default_keyspace"

# Initialize our vector db
astra_db = AstraDB(token=token, api_endpoint=api_endpoint, namespace=keyspace)
astra_db.create_collection(collection_name=collection_name, dimension=dimension)
