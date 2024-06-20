from elasticsearch import Elasticsearch
from getpass import getpass  # For securely getting user input
from elasticsearch import MlClient
import os

# connecting to the elastic client with your credentials
def connect_client():
    # Using environment variables for the Elastic Cloud ID and API Key; 
    # alternatively use getpass("Elastic Cloud ID: ") to type out the auth details interactively
    ELASTIC_CLOUD_ID = getpass("Elastic Cloud ID: ")
    ELASTIC_API_KEY = getpass("Elastic API Key: ")

    # Create an Elasticsearch client using the provided credentials
    client = Elasticsearch(
        cloud_id="1cbae2c8e21b4247bfebe86ced9125f0:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDg3YzVhYjc1ODE0NTRmMzFiZGNlMmRjYTkxMzMxYzk0JDUzMzYwMzg3NTA4YTQ3MjRhYmNiMDQ1ZWZjYjg0MGU5",  # cloud id can be found under deployment management
        api_key="d2xiLUxKQUJ6eF9NZGRpMWdxb3o6QVF5dXA0bmVTWmFsNXRwSEJtYjR0dw==" # API keys can be generated under management / security
    )

    print(client.info())
    return client

# running semantic search
def semantic_search(question, client, model_id, index):
    question = {"text_field" : question}
    result = MlClient.infer_trained_model(client, model_id =model_id, docs = question)
    query_vector = result["inference_results"][0]["predicted_value"]

    query = {
        "field": "text_embedding.predicted_value",
        "query_vector": query_vector,
        "k": 5,
        "num_candidates": 100
    }
    
    #you can modify the fields you want returned or add these to the parameters of the function as well
    result = client.search(index = index, knn=query, source=["Sentence", "Character"])     
    answer = []
    for element in result["hits"]["hits"]:
        answer.append("{}: {}, score {}".format(element["_source"]["Character"], element["_source"]["Sentence"], element["_score"]))

    return answer