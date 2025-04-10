import os
import sys

from dotenv import load_dotenv

from astrapy import DataAPIClient
from astrapy.info import CollectionDefinition

load_dotenv()

# Grab the Astra token and api endpoint from the environment
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
keyspace = os.getenv("ASTRA_DB_KEYSPACE")
collection_name = os.getenv("ASTRA_DB_COLLECTION")
dimension_str = os.getenv("VECTOR_DIMENSION")

# check that the dimension is defined and is an integer
if dimension_str is None:
    print("environment variable 'VECTOR_DIMENSION' not defined")
    sys.exit()
else:
    if not dimension_str.isdigit():
        print("environment variable 'VECTOR_DIMENSION' not integer")
        sys.exit()

astra_db_client = DataAPIClient()
database = astra_db_client.get_database(
    api_endpoint,
    token=token,
    keyspace=keyspace,
)

collection = database.create_collection(
    collection_name,
    definition=(
        CollectionDefinition.builder().set_vector_dimension(int(dimension_str)).build()
    ),
)

print(f"Collection {collection.name} created successfully.")
