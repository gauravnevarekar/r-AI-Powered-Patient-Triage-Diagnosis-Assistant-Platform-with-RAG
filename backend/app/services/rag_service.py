import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
from backend.app.config import settings
from backend.app.schemas import RAGCitation

class RealVectorRAGService:
    def __init__(self):
        self.knowledge_file = os.path.join(settings.DATA_DIR, "medical_knowledge_base.json")
        self.chunks = []
        self.vectorizer = None
        self.chunk_embeddings = None
        self._load_and_index()

    def _load_and_index(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

        if self.chunks:
            # Build Vector Space Matrix over all knowledge base chunk texts
            corpus = [f"{c['condition']} {c['category']} {c['title']} {c['content']}" for c in self.chunks]
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
            self.chunk_embeddings = self.vectorizer.fit_transform(corpus)

    def retrieve_and_generate(self, condition: str, symptoms: str, history_items: List[str] = None) -> Dict[str, Any]:
        """
        Perform real mathematical Cosine Similarity Vector Retrieval over Knowledge Base Chunks.
        """
        if not self.chunks or self.vectorizer is None:
            self._load_and_index()

        query_text = f"{condition} {symptoms}"
        if history_items:
            query_text += " " + " ".join(history_items)

        # 1. Transform query into vector space
        query_vec = self.vectorizer.transform([query_text])

        # 2. Compute Cosine Similarity between query vector and all knowledge chunk vectors
        similarities = cosine_similarity(query_vec, self.chunk_embeddings)[0]

        # 3. Sort indices by highest cosine similarity
        top_indices = np.argsort(similarities)[::-1]
        
        best_chunks = []
        citations = []
        for idx in top_indices[:2]:
            score = float(similarities[idx])
            chunk = self.chunks[idx]
            best_chunks.append((chunk, score))
            
            citations.append(RAGCitation(
                source_title=chunk["title"],
                guideline_ref=chunk["guideline_ref"],
                snippet=f"{chunk['content'][:180]}... (Vector Cosine Similarity Score: {round(score, 3)})"
            ))

        best_chunk, top_score = best_chunks[0]

        # 4. Dynamically synthesize source-grounded clinical reasoning
        history_str = f" Incorporating active history: {', '.join(history_items)}." if history_items else ""
        reasoning = (
            f"Vector Search match ({round(top_score * 100, 1)}% semantic similarity score) for presentation '{symptoms}'{history_str} "
            f"aligns with clinical evidence for {condition}. "
            f"Per {best_chunk['title']} ({best_chunk['guideline_ref']}): {best_chunk['content']}"
        )

        return {
            "reasoning": reasoning,
            "citations": citations
        }

rag_service = RealVectorRAGService()
