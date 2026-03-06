def format_data(filename, data, statistics):
    return {
        "document": {
            "filename": filename,
            "total_characters": statistics["total_chars"],
            "total_words": statistics["total_words"],
            "total_sentences": statistics["total_sentences"]
        },
        "content": {
            "cleaned_text": data['text'],
            "tokens": data["tokens"],
        },
        "statistics": {
            "word_frequencies": statistics["word_frequencies"],
            "top_10_words": statistics["top_words"],
        }
    }