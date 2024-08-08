import pickle
import torch
from sentence_transformers import SentenceTransformer, util

# Load the embeddings and metadata
with open('data/embeddings_with_metadata.pkl', 'rb') as f:
    data = pickle.load(f)

corpus_embeddings = torch.tensor(data['embeddings'])
metadata = data['metadata']

embedder = SentenceTransformer("all-MiniLM-L6-v2")

savedProductLen = len(corpus_embeddings)
top_k = min(5, savedProductLen)

def searchquery(queries):
    high_scoring_products = []
    
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)
    
        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)
    
        print("\nQuery:", query)
        print(top_results)
    
        for score, idx in zip(top_results[0], top_results[1]):
            product = metadata[idx.item()]
            print(f"Product ID: {product['PRODUCTID']}")
            print(f"Name: {product['NAME']}")
            print(f"Score: {score:.4f}")
            print("---")
            
            if score > 0.5:
                high_scoring_products.append(query+  "   "  + product['NAME'] + "   " + product['PRODUCTID'])
    
    return high_scoring_products

