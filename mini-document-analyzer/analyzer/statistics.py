def count_sentences(text: str):
    punctuation = ".?!"
    count = sum(1 for char in text if char in punctuation)

    return count