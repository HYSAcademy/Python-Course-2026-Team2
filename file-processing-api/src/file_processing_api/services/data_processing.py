import string
from nltk.corpus import stopwords

def clean_text(text: str):
    text = text.lower().strip()
    trans = text.maketrans("", "", string.punctuation)

    return text.translate(trans)