def count_sentences(text: str):
    punctuation = ".?!"
    count = sum(1 for char in text if char in punctuation)

    return count

def count_word_frequencies(words: list[str]):
    word_frequencies = {}

    for word in words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    return word_frequencies