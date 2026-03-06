import string

def clean_text(text: str):
    text = text.lower().strip()
    trans = text.maketrans("", "", string.punctuation)

    return text.translate(trans)

def get_modified_data(text: str):
    cleaned = clean_text(text)
    tokens = cleaned.split()

    return {
        "text": cleaned,
        "tokens": tokens
    }