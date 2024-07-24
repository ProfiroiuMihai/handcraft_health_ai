from constant import EMBEDDINGS, CHAT_LLM, SYSTEM_PROMPT, index


def get_query_embeddings(query: str) -> list[float]:
    """This function returns a list of the embeddings for a given query"""
    query_embeddings = EMBEDDINGS.embed_query(query)
    return query_embeddings


def query_pinecone_index(
    query_embeddings: list, top_k: int = 2, include_metadata: bool = True
) -> dict[str, any]:
    """Query a Pinecone index."""
    query_response = index.query(
        vector=query_embeddings, top_k=top_k, include_metadata=include_metadata
    )
    return query_response


def better_query_response(prompt: str) -> str:
    """This function returns a better response using LLM"""
    better_answer = CHAT_LLM(prompt)
    return better_answer