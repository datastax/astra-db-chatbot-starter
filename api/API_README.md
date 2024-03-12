## API Readme

# Setup

This readme is for a FastAPI api that uses pydantic to parse incoming data. That data is used to retreive documents from an Astra vector store and then both the original query and the user input are used to construct a prompt. That prompt is sent to OpenAI and the api returns the response to the user.

Then clone this repo and install the Python requirements (This demo assumes you already have python3 installed):
```
git clone https://github.com/Anant/astra-chatbot-react-python.git
pip3 install -r requirements.txt
```

Input all authentication credentials into .env file. This file requires below Astra information.

    - ASTRA_DB_APPLICATION_TOKEN=Generate app token for Astra database
    - ASTRA_DB_NAMESPACE=existing Astra DB namespace in vector databaseB
    - ASTRA_DB_API_ENDPOINT="https://ASTRA_DB_ID-ASTRA_REGIN.apps.astra.datastax.com
    - ASTRA_DB_COLLECTION=Name of collection/table to be created in Astra database
    - VECTOR_DIMENSION=Collection to be created with number of vector dimensions
    - SCRAPED_FILE=Scraped data file location
    - OPENAI_API_KEY=api key for OPENAI
    - VECTOR_MODEL = Vector Model to be used. Future, models are expected to change due to deprecation and expect new model to be used 

# Start Process

To run the api enter the command:
```
uvicorn api.index:app --reload
```
