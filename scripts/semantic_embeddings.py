import os


def compute_semantic_embedding_vector(text: str):
    import openai
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise Exception("OPENAI_API_KEY environment variable not set.")
    client = openai.Client(
        api_key=OPENAI_API_KEY,
    )
    model = 'text-embedding-3-small'
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
