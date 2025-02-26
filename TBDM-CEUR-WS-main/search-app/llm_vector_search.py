import os
from pymongo.mongo_client import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import json


class LLMVectorSearch:
    # Initialize MongoDB, Vector Model and Gemini Model
    client = MongoClient(os.getenv('DATABASE_URL'))
    vector_model = SentenceTransformer('microsoft/mpnet-base')
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')

    # Define MongoDB Databse and Collection
    db_name = "ceur_ws"
    collection_name = "vector_records"

    def search(self, query):
        print("User Query: ", query)
        # Create Vector Query
        vector_query = self.vector_model.encode(query).tolist()
        print("Vector Query: ", vector_query)

        # Query the index based on embedding similarity
        pipeline = [
            {
                "$search": {
                    "index":"default",
                    "knnBeta": {
                        "vector": vector_query,
                        "path": "embedding",
                        "k": 5,
                    }
                }
            },
            {
                "$project": {
                    "embedding": 0,
                    "_id": 0,
                    "score": {
                        "$meta": "searchScore"
                    },
                }
            }
        ]
        results = list(self.client[self.db_name][self.collection_name].aggregate(pipeline))
        context = json.dumps(results)
        print("MongoDB Query Result: ", context)

        # Generate LLM Output using Gemini model
        prompt = f"""You are a useful assistant. Use the assistant's content to answer the user's query. Summarize your answer using the provided context and cite any relevant 'page_number' and 'filename' metadata in your reply.
        Context: {context}
        Query: {query}
        """
        response = self.gemini_model.generate_content(prompt)
        text = response.text
        print("LLM Reponse: ", text)
      
        return text