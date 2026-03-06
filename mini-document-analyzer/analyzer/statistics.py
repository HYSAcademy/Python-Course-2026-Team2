def count_sentences(text: str):
    punctuation = ".?!"
    count = sum(1 for char in text if char in punctuation)

    return count

def count_word_frequencies(words: list[str]):
    word_frequencies = {}

    for word in words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    return word_frequencies

def get_top_words(frequencies: dict[str, int], quantity: int = 10):
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    return [list(freq) for freq in sorted_frequencies[:quantity]]