from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

import os
from dotenv import load_dotenv
from astrapy.db import AstraDBCollection

load_dotenv()

# Grab the Astra token and api endpoint from the environment
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
namespace = os.getenv("ASTRA_DB_NAMESPACE")
openai_api_key = os.getenv("OPENAI_API_KEY")
collection_name = os.getenv("ASTRA_DB_COLLECTION")
model = os.getenv("VECTOR_MODEL")

# langchain openai interface
llm = OpenAI(openai_api_key=openai_api_key)

if not model:
    embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
else:
    embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key, model=model)

def get_similar_docs(query, number):
    if not namespace:
        collection = AstraDBCollection(collection_name=collection_name, token=token,
                                       api_endpoint=api_endpoint)
    else:
        collection = AstraDBCollection(collection_name=collection_name, token=token,
                                       api_endpoint=api_endpoint, namespace=namespace)
    embedding = list(embedding_model.embed_query(query))
    relevant_docs = collection.vector_find(embedding, limit=number)

    docs_contents = [row['answer'] for row in relevant_docs]
    docs_urls = [row['document_id'] for row in relevant_docs]
    return docs_contents, docs_urls

# prompt that is sent to openai using the response from the vector database and the users original query
prompt_boilerplate = "Answer the question posed in the user query section using the provided context"
user_query_boilerplate = "USER QUERY: "
document_context_boilerplate = "CONTEXT: "
final_answer_boilerplate = "Final Answer: "

def build_full_prompt(query):
    relevant_docs, urls = get_similar_docs(query, 3)
    docs_single_string = "\n".join(relevant_docs)
    url = urls[0] # set(urls)

    nl = "\n"
    filled_prompt_template = prompt_boilerplate + nl + user_query_boilerplate+ query + nl + document_context_boilerplate + docs_single_string + nl + final_answer_boilerplate
    print(filled_prompt_template)
    return filled_prompt_template, url

def send_to_openai(full_prompt):
    return llm.invoke(full_prompt)

