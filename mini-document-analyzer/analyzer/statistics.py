from typing import Any
import re


def count_sentences(text: str) -> int:
    s_list = re.split(r"[.?!]+", text)
    sentences = [s.strip() for s in s_list if s.strip()]

    return len(sentences)

def count_word_frequencies(words: list[str]) -> dict[str, int]:
    word_frequencies = {}

    for word in words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    return word_frequencies

def get_top_words(frequencies: dict[str, int], quantity: int = 10) -> list[list[str | int]]:
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    return [list(freq) for freq in sorted_frequencies[:quantity]]

def get_statistics(words: list[str], raw_text: str) -> dict[str, Any]:
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