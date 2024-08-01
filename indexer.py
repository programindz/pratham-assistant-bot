from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from scraper import run_scraper

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_sentence_embeddings_with_faiss():
    all_paragraphs = run_scraper()

    all_paragraph_embeddings = embedding_model.encode(all_paragraphs)
    embedding_matrix = np.array(all_paragraph_embeddings).astype('float32')

    index = faiss.IndexFlatL2(embedding_matrix.shape[1])
    index.add(embedding_matrix)
    
    return index, all_paragraphs


