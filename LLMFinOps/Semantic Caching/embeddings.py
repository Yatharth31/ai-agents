import os
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# 1. Load a pretrained Sentence Transformer model
model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# The sentences to encode read from file
with open('user-queries.txt', 'r') as file:
    # Read all lines into a list
    sentences = [line.strip() for line in file]
# print(sentences[:11])

api_query_url = f"https://router.huggingface.co/hf-inference/models/{model_id}/pipeline/feature-extraction"
api_similarity_url = f"https://router.huggingface.co/hf-inference/models/{model_id}/pipeline/sentence-similarity"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(texts):
    response = requests.post(api_query_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()

# 2. Calculate embeddings by model api call
embeddings = query(sentences)
embeddings = np.array(embeddings)
# print(embeddings.shape)
# [3, 384]

# 3. local run function to calculate cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

embeddings = np.array(embeddings)

similarities = np.zeros((len(embeddings), len(embeddings)))

for i in range(len(embeddings)):
    for j in range(len(embeddings)):
        similarities[i][j] = cosine_similarity(
            embeddings[i],
            embeddings[j]
        )

# print(similarities)
# print(similarities.shape)

# 4. Semantic search
search_query = "What is the weather like tomorrow?"

# Get embedding for the search query
query_embedding = np.array(query([search_query]))[0]

# Calculate similarity between query and every sentence
search_scores = np.array([
    cosine_similarity(query_embedding, embedding)
    for embedding in embeddings
])

# Rank sentences by similarity
ranked_indices = np.argsort(search_scores)[::-1]

# Display results
print("\nSemantic Search Results:")
for i in ranked_indices[:5]:
    print(f"{search_scores[i]:.4f} → {sentences[i]}")