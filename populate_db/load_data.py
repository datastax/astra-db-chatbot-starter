import json
import os

import split_q_and_a

from langchain_openai import OpenAIEmbeddings

import time

from dotenv import load_dotenv
from astrapy.db import AstraDBCollection

#To do: add logger

load_dotenv()

# Grab the Astra token and api endpoint from the environment
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
keyspace = os.getenv("ASTRA_DB_NAMESPACE")
openai_api_key = os.getenv("OPENAI_API_KEY")
collection_name = os.getenv("ASTRA_DB_COLLECTION")
dimension = os.getenv("VECTOR_DIMENSION")
openai_api_key=os.getenv("OPENAI_API_KEY")
input_data = os.getenv("SCRAPED_FILE")
model = os.getenv("VECTOR_MODEL")

if not model:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
else:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model=model)

def get_input_data():
    scraped_results_file = input_data
    with open(scraped_results_file) as f:
        scraped_data = json.load(f)

        faq_scraped_data = []
        for d in scraped_data:
            if "faq" in d["url"].lower():
                faq_scraped_data.append(d)
    return faq_scraped_data

def embed(text_to_embed):
    embedding = list(embeddings.embed_query(text_to_embed))
    return embedding

def main():
    if not keyspace:
        collection = AstraDBCollection(collection_name=collection_name, token=token,
                                       api_endpoint=api_endpoint)
    else:
        collection = AstraDBCollection(collection_name=collection_name, token=token,
                                       api_endpoint=api_endpoint, namespace=keyspace)

    input_data_faq = get_input_data()

    # process faq data
    for webpage in input_data_faq:
        q_and_a_data = split_q_and_a.split(webpage)
        for i in range (0,len(q_and_a_data["questions"])):
            document_id = webpage["url"]
            question_id = i + 1
            question = q_and_a_data["questions"][i]
            answer = q_and_a_data["answers"][i]
            text_to_embed = f"{question}"
            embedding = embed(text_to_embed)
            time.sleep(1)
            to_insert = {"document_id": document_id, "question_id": question_id, "answer": answer,
                             "question": question, "$vector": embedding}
            if (question == " Cluster?") or (question == "?"):
                print("Malformed question. Not adding to vector db.")
            else:
                result = collection.insert_one(to_insert)
                print(f"{result} \tdocument_id: {document_id} question_id: {question_id}")

if __name__ == "__main__":
    main()
