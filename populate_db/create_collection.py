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
