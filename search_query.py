from sentence_transformers import SentenceTransformer
import torch

embedder = SentenceTransformer("all-MiniLM-L6-v2")

savedProductLen=10

top_k = min(5, savedProductLen)

def searchquery(queries):
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)
    
        # We use cosine-similarity and torch.topk to find the highest 5 scores
        similarity_scores = embedder.similarity(query_embedding, corpus_embeddings)[0]
        scores, indices = torch.topk(similarity_scores, k=top_k)
    
        print("\nQuery:", query)
        print("Top 5 most similar sentences in corpus:")
    
        for score, idx in zip(scores, indices):
            print(corpus[idx], "(Score: {:.4f})".format(score))