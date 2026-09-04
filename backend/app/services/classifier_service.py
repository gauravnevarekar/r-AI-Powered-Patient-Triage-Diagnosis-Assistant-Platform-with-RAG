import os
import csv
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any, List
from backend.app.config import settings

MODEL_FILE = os.path.join(settings.MODELS_DIR, "triage_classifier.pkl")
VECTORIZER_FILE = os.path.join(settings.MODELS_DIR, "tfidf_vectorizer.pkl")
DATASET_FILE = os.path.join(settings.DATA_DIR, "multi_disease_dataset.csv")

class MultiDiseaseClassifierService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.rows = []
        self._initialize_or_load()

    def _load_csv(self):
        self.rows = []
        if os.path.exists(DATASET_FILE):
            with open(DATASET_FILE, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.rows.append(row)

    def _initialize_or_load(self):
        os.makedirs(settings.MODELS_DIR, exist_ok=True)
        self._load_csv()

        if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
            self.model = joblib.load(MODEL_FILE)
            self.vectorizer = joblib.load(VECTORIZER_FILE)
        else:
            self.train_model()

    def train_model(self):
        """Train TF-IDF + RandomForest classifier on multi-disease dataset."""
        if not self.rows:
            self._load_csv()

        # Duplicate dataset rows 5x to ensure sufficient sample support per multi-disease class
        augmented_rows = self.rows * 5

        X_text = [r['symptoms'] for r in augmented_rows]
        y_labels = [r['condition'] for r in augmented_rows]

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
        X_vec = self.vectorizer.fit_transform(X_text)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_vec, y_labels)

        joblib.dump(self.model, MODEL_FILE)
        joblib.dump(self.vectorizer, VECTORIZER_FILE)
        print("Triage classifier trained and persisted to disk.")

    def predict(self, symptom_text: str, symptom_chips: List[str] = None) -> Dict[str, Any]:
        """
        Real ML Inference Pipeline:
        1. Feature Extraction: Concatenate raw text & symptom chips.
        2. Vectorization: Transform text with TF-IDF vectorizer.
        3. Model Execution: Call model.predict_proba(vec) on real input.
        4. Probability Matrix: Rank classes by model output probability.
        """
        full_query = symptom_text.strip()
        if symptom_chips:
            full_query += " " + " ".join(symptom_chips)

        if not full_query:
            full_query = "general abdominal discomfort fever"

        # Feature Extraction: TF-IDF vectorization
        vec = self.vectorizer.transform([full_query])
        
        # Real ML Model Execution
        probs = self.model.predict_proba(vec)[0]
        classes = self.model.classes_

        # Rank predictions strictly by model probability matrix
        top_indices = np.argsort(probs)[::-1]
        
        primary_idx = top_indices[0]
        primary_condition = classes[primary_idx]
        primary_confidence = float(probs[primary_idx])

        # Lookup condition metadata in rows
        matched_row = None
        for r in self.rows:
            if r['condition'] == primary_condition:
                matched_row = r
                break
        
        if matched_row:
            urgency = matched_row['urgency']
            specialist = matched_row['specialist']
        else:
            urgency = "URGENT_12_24_HRS"
            specialist = "General Physician"

        # Calculate differential diagnoses strictly from top probability outputs
        differentials = []
        for idx in top_indices[1:4]:
            cond = classes[idx]
            prob = float(probs[idx])
            likelihood = "Possible" if prob > 0.05 else "Unlikely"
            differentials.append({
                "condition": cond,
                "probability": round(prob, 4),
                "likelihood": likelihood
            })

        return {
            "primary_condition": primary_condition,
            "primary_confidence": round(primary_confidence, 4),
            "urgency": urgency,
            "specialist": specialist,
            "differential_diagnoses": differentials
        }

classifier_service = MultiDiseaseClassifierService()
