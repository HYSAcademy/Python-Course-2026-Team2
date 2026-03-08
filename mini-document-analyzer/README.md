# Mini Document Analyzer

## Project Overview
**Mini Document Analyzer** is a CLI-based Python application that analyzes `.txt` documents and generates structured JSON output. The tool helps extract text statistics, clean content, and provide word frequency insights.

---

## Features

- Accepts a `.txt` file as input
- Converts text to lowercase and removes punctuation
- Tokenizes text into words
- Calculates:
  - Total characters (including spaces)
  - Total words
  - Total sentences (., !, ?)
  - Word frequency dictionary
  - Top 10 most frequent words
- Generates structured JSON output
- Handles CLI argument parsing and input validation
- Provides clear error messages for invalid input

---
## CLI Usage # Basic usage
```
python main.py input.txt
```
# Specify output JSON file
```
python main.py input.txt output.json
```
* If the output file is not provided, it defaults to: input.analysis.json ---
## Example JSON Output
```json
{
  "document": {
    "filename": "input.txt",
    "total_characters": 1024,
    "total_words": 180,
    "total_sentences": 12
  },
  "content": {
    "cleaned_text": "this is example text without punctuation",
    "tokens": ["this", "is", "example", "text"]
  },
  "statistics": {
    "word_frequencies": {
      "example": 5,
      "text": 4
    },
    "top_10_words": [
      ["example", 5],
      ["text", 4]
    ]
  }
}
```
## Project Structure
```
mini-document-analyzer/
│
├── analyzer/
│   ├── __init__.py
│   ├── text_reader.py
│   ├── tokenizer.py
│   ├── statistics.py
│
├── cli.py
├── main.py
├── README.md
└── .gitignore
```
### 3️⃣ Team table 

| Developer           | Responsibility                                                            |
| ------------------- | ------------------------------------------------------------------------- |
| Kateryna Hryhorieva | Core logic: file reading, text cleaning, tokenization, statistics         |
| Kostiantyn Yesypenko | CLI parsing, input validation, JSON export, error handling, documentation |

---
