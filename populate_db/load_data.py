import json
import os

import split_q_and_a
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from astrapy import DataAPIClient

# To do: add logger

load_dotenv()

# Grab the Astra token and api endpoint from the environment
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
keyspace = os.getenv("ASTRA_DB_KEYSPACE")
openai_api_key = os.getenv("OPENAI_API_KEY")
collection_name = os.getenv("ASTRA_DB_COLLECTION")
dimension = os.getenv("VECTOR_DIMENSION")
openai_api_key = os.getenv("OPENAI_API_KEY")
input_data = os.getenv("SCRAPED_FILE")
model = os.getenv("VECTOR_MODEL")

EMBEDDING_CHUNK_SIZE = 80


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
    return embeddings.embed_query(text_to_embed)


def embed_list(texts_to_embed):
    return embeddings.embed_documents(texts_to_embed)


def main():
    astra_db_client = DataAPIClient()
    database = astra_db_client.get_database(
        api_endpoint,
        token=token,
        keyspace=keyspace,
    )
    collection = database.get_collection(collection_name)

    input_data_faq = get_input_data()[:20]

    # process faq data. First collect all information, then embed in chunks
    reformatted_documents = []
    for webpage in input_data_faq:
        q_and_a_data = split_q_and_a.split(webpage)
        for i in range(0, len(q_and_a_data["questions"])):
            document_id = webpage["url"]
            question_id = i + 1
            question = q_and_a_data["questions"][i]
            answer = q_and_a_data["answers"][i]
            to_insert = {
                "document_id": document_id,
                "question_id": question_id,
                "answer": answer,
                "question": question,
            }
            if (question == " Cluster?") or (question == "?"):
                print("Malformed question. Not adding to vector db.")
            else:
                reformatted_documents.append(to_insert)

    # compute a matching list of embeddings, then pair them with their document
    print(f"Computing embeddings for {len(reformatted_documents)} questions...")
    embedding_vectors = []
    for chunk_start in range(0, len(reformatted_documents), EMBEDDING_CHUNK_SIZE):
        chunk = reformatted_documents[chunk_start : chunk_start + EMBEDDING_CHUNK_SIZE]
        to_embed_strings = [doc_to_insert["question"] for doc_to_insert in chunk]
        chunk_embedding_vectors = embed_list(to_embed_strings)
        embedding_vectors += chunk_embedding_vectors

    assert len(embedding_vectors) == len(reformatted_documents)
    final_documents_to_insert = [
        {
            "$vector": emb_vec,
            **ref_doc,
        }
        for ref_doc, emb_vec in zip(reformatted_documents, embedding_vectors)
    ]

    insertion_result = collection.insert_many(final_documents_to_insert)
    print(f"Insertion result: {insertion_result}")


if __name__ == "__main__":
    main()
