# CODE DUMPSSSS
# 3. Calculate the embedding similarities using api call
def calculate_similarity(source_sentence, sentences):
    payload = {
        "inputs": {
            "source_sentence": source_sentence,
            "sentences": sentences
        }
    }

    response = requests.post(
        api_similarity_url,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print("Error:", response.text)
        response.raise_for_status()

    return response.json()

# similarities = calculate_similarity(embeddings, embeddings)

# print(similarities)