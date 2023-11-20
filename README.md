# Astra DB Chatbot Starter

For the full instructions, see the [Build a chatbot with LangChain tutorial](https://docs.datastax.com/en/astra/astra-db-vector/tutorials/chatbot.html) in the DataStax docs.

## Setting up your database and seeding with data
1. [Create or sign in](https://astra.datastax.com/register) to your Astra account.
2. Create a vector database. Store the database id, region, and token for later.
3. [Create or sign in](https://platform.openai.com/) to your OpenAI account. Store your OpenAI key for later.
4. Navigate to your IDE, set up the following environment variables:

- ASTRA_DB_NAMESPACE=default_keyspace (or an existing Astra keyspace in a vector-enabled database)
- OPENAI_API_KEY=api key for OPENAI
- ASTRA_DB_ID=Astra DB database id
- ASTRA_DB_REGION=Astra DB database region
- ASTRA_DB_APPLICATION_TOKEN=Generate app token for Astra database

5. Install Python dependencies:

```
pip install -r requirements.txt
```

6. Run the collection creation script:
```
python populate_db/create_collection.py
```
7. Run the data loading script:
```
python populate_db/load_data.py
```

8. Click to deploy the app to Vercel: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/datastax/astra-db-chatbot-starter&env=ASTRA_DB_NAMESPACE,OPENAI_API_KEY,ASTRA_DB_ID,ASTRA_DB_REGION,ASTRA_DB_APPLICATION_TOKEN).
  
   Set your environment variables to the values created in step 4.
