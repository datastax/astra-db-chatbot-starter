# Astra DB Chatbot Starter

## Getting Started with Vercel

1. [Create or sign in](https://astra.datastax.com/register) to your Astra DB account.
2. Create a vector database. Store the database id, region and namespace, and token for later.
3. [Create or sign in](https://platform.openai.com/) to your OpenAI account. Store your OpenAI key for later.
4. Click to deploy the app to Vercel: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/datastax/astra-db-chatbot-starter&env=ASTRA_DB_NAMESPACE,OPENAI_API_KEY,ASTRA_DB_ID,ASTRA_DB_REGION,ASTRA_DB_APPLICATION_TOKEN).
  
   Set your environment variables to the values created in steps 1 and 3.
##
Set python virtual environment on linux
   apt-get install python3.11-venv
   python3 -m venv venv
   source venv/bin/activate
   clone repository and install all requirements.txt

## Setting up your database and seeding with data
1. Navigate to your IDE, set up the following environment variables:

- ASTRA_DB_APPLICATION_TOKEN=Generate app token for Astra database
- ASTRA_DB_NAMESPACE=existing Astra DB namespace in vector database
- ASTRA_DB_API_ENDPOINT="https://ASTRA_DB_ID-ASTRA_REGION.apps.astra.datastax.com"
- ASTRA_DB_COLLECTION=Name of collection/table to be created in Astra database
- VECTOR_DIMENSION=Collection to be created with number of vector dimensions
- SCRAPED_FILE=Scraped data file location
- OPENAI_API_KEY=api key for OPENAI
- VECTOR_MODEL = Vector Model to be used. Future, models are expected to change due to deprecation and expect new model to be used 

2. Install Python dependencies:

```
pip install -r requirements.txt
```

3. Run the collection creation script:
```
python populate_db/create_collection.py
```
4. Run the data loading script:
```
python populate_db/load_data.py
```
