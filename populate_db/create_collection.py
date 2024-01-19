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
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
else:
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint, namespace=keyspace)

astra_db.create_collection(collection_name=collection_name, dimension=dimension)

if collection_name in astra_db.get_collections()['status']['collections']:
    print(f"Collection '{collection_name}' already exists. New collection not created")
else:
    astra_db.create_collection(collection_name=collection_name, dimension=dimension)
