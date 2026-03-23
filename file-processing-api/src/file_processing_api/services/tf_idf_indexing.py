import numpy as np
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.matrix = None
        self.documents = []

    def fit(self, documents: list[str]):
        self.documents = documents
        self.matrix = self.vectorizer.fit_transform(documents)

    def transform(self, documents: list[str]):
        return self.vectorizer.transform(documents)

    def get_similarities(self, query_vec, vectors):
        stored_matrix = np.vstack([
            v.vector.toarray()[0] if hasattr(v.vector, "toarray") else v.vector
            for v in vectors
        ])

        return cosine_similarity(query_vec, stored_matrix).flatten()

tfidf_service = TFIDFService()