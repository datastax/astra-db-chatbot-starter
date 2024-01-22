import os
import sys

from dotenv import load_dotenv

from astrapy.db import AstraDB

load_dotenv()

# Grab the Astra token and api endpoint from the environment
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
keyspace = os.getenv("ASTRA_DB_KEYSPACE")
collection_name = os.getenv("ASTRA_DB_COLLECTION_NAME")
dimension = os.getenv("VECTOR_DIMENSION")

# check that dimension is defined and is an integer
if dimension == None:
    print("environment variable 'VECTOR_DIMENSION' not defined")
    sys.exit()
else:
    if not dimension.isdigit():
        print("environment variable 'VECTOR_DIMENSION' not integer")
        sys.exit()

# check that keyspace is defined
if not keyspace:
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
else:
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint, namespace=keyspace)

# create collection if it doesn't exist
if collection_name in astra_db.get_collections()['status']['collections']:
    print(f"Collection '{collection_name}' already exists. New collection not created")
else:
    astra_db.create_collection(collection_name=collection_name, dimension=dimension)
