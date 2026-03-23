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
        vocab_size = len(self.vectorizer.vocabulary_)

        rows = []
        for v in vectors:
            dense = np.zeros(vocab_size, dtype=float)
            for idx, score in v.vector.items():
                dense[int(idx)] = score
            rows.append(dense)

        stored_matrix = np.vstack(rows)
        return cosine_similarity(query_vec, stored_matrix).flatten()

tfidf_service = TFIDFService()