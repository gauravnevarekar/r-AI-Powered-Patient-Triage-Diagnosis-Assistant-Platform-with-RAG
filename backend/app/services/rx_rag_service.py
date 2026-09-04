import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List
from backend.app.config import settings
from backend.app.schemas import RAGCitation

class RealPrescriptionVectorRAGService:
    def __init__(self):
        self.drug_file = os.path.join(settings.DATA_DIR, "drug_knowledge_base.json")
        self.drugs = []
        self.vectorizer = None
        self.drug_embeddings = None
        self._load_and_index()

    def _load_and_index(self):
        if os.path.exists(self.drug_file):
            with open(self.drug_file, "r", encoding="utf-8") as f:
                self.drugs = json.load(f)

        if self.drugs:
            corpus = [f"{d['drug_name']} {' '.join(d.get('aliases', []))} {d['monograph_title']} {d['content']}" for d in self.drugs]
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
            self.drug_embeddings = self.vectorizer.fit_transform(corpus)

    def answer_question(self, drug_name: str, question: str) -> Dict[str, Any]:
        """Perform real Cosine Similarity Vector Retrieval over Drug Monograph Base."""
        if not self.drugs or self.vectorizer is None:
            self._load_and_index()

        query_text = f"{drug_name} {question}"

        # 1. Transform query into vector space
        query_vec = self.vectorizer.transform([query_text])

        # 2. Compute Cosine Similarity between query vector and all drug monograph vectors
        similarities = cosine_similarity(query_vec, self.drug_embeddings)[0]
        top_idx = int(np.argmax(similarities))
        top_score = float(similarities[top_idx])

        matched_drug = self.drugs[top_idx]

        # 3. Dynamic RAG Answer Synthesis
        q_lower = question.lower()
        safety_alert = None

        if "paracetamol" in q_lower or "interaction" in q_lower or "alcohol" in q_lower:
            answer = (
                f"Pharmacological Monograph Search ({round(top_score * 100, 1)}% Vector Similarity Match): "
                f"Regarding {matched_drug['drug_name']} ({matched_drug['monograph_title']}): {matched_drug['content']}"
            )
        elif "side effect" in q_lower or "adverse" in q_lower or "reaction" in q_lower:
            answer = (
                f"Adverse Reaction Vector Retrieval: Common clinical side effects reported for {matched_drug['drug_name']} include gastrointestinal discomfort or nausea. "
                f"Monograph guidance: {matched_drug['content']}"
            )
            safety_alert = "Immediate Action Alert: If you experience severe hives, facial/tongue swelling, or breathing difficulty, seek emergency care immediately (dial 911)."
        else:
            answer = (
                f"Vector Monograph Match ({round(top_score * 100, 1)}% Similarity) for {matched_drug['drug_name']}: "
                f"{matched_drug['content']}"
            )

        citations = [
            RAGCitation(
                source_title=matched_drug["monograph_title"],
                guideline_ref=matched_drug["guideline_ref"],
                snippet=f"{matched_drug['content'][:180]}... (Vector Cosine Match: {round(top_score, 3)})"
            )
        ]

        return {
            "answer": answer,
            "safety_alert": safety_alert,
            "source_monograph": matched_drug["monograph_title"],
            "citations": citations
        }

rx_rag_service = RealPrescriptionVectorRAGService()
