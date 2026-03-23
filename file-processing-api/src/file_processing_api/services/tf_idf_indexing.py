from sklearn.feature_extraction.text import TfidfVectorizer


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
