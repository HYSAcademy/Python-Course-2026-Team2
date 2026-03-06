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

def get_statistics(words: list, raw_text: str):
    total_sentences = count_sentences(raw_text)
    word_frequencies = count_word_frequencies(words)
    top_words = get_top_words(word_frequencies)

    return {
        'total_chars': len(raw_text),
        'total_words': len(words),
        'total_sentences': total_sentences,
        'word_frequencies': word_frequencies,
        'top_words': top_words,
    }