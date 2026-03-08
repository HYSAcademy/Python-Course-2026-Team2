import json
import os
import argparse
from analyzer.text_reader import read_file
from analyzer.tokenizer import get_modified_data
from analyzer.statistics import get_statistics
from formatter import format_data

def validate_input_file(input_file: str) -> bool:
    """Checks whether the file exists, whether it is a TXT file, and whether it is empty."""
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return False
    if not input_file.endswith(".txt"):
        print("Error: Input file must be a TXT file.")
        return False
    if os.stat(input_file).st_size == 0:
        print(f"Error: File '{input_file}' is empty.")
        return False
    return True

def get_output_file(input_file: str, output_arg: str | None) -> str:
    """Return the path to the output JSON file.

    If `output_arg` is not provided, the input filename (without its
    extension) is used with the suffix `.analysis.json` appended.
    If `output_arg` is given, any extension is stripped and `.json` is
    added to the base name (so `report.txt` or `report.json` both produce
    `report.json`).
    """
    if output_arg:
        base = os.path.splitext(output_arg)[0]
        return f"{base}.json"
    return f"{os.path.splitext(input_file)[0]}.analysis.json"

def export_json(data, output_file):
    """Exports data to a JSON file with indentation."""
    if not data:
        print("Error: No data to export.")
        return
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def run_cli():
    """
    CLI for Mini Document Analyzer.

    Usage:
        python main.py input.txt
        python main.py input.txt output.json
    """
    parser = argparse.ArgumentParser(description="Mini Document Analyzer")
    parser.add_argument("input", help="Path to input TXT file")
    parser.add_argument(
        "output",
        nargs="?",  
        help="Optional output JSON filename"
    )
    args = parser.parse_args()

    input_file = args.input
    output_file = get_output_file(input_file, args.output)

    # --- VALIDATION ---
    if not validate_input_file(input_file):
        return

    # --- ANALYSIS PIPELINE ---
    try:
        content = read_file(input_file)
        if not content.strip():
            print("Error: File contains only whitespace.")
            return
        data = get_modified_data(content)
        statistics = get_statistics(data['tokens'], content)
        output = format_data(input_file, data, statistics)
    except Exception as e:
        print(f"Error during analysis: {e}")
        return

    # --- JSON EXPORT ---
    export_json(output, output_file)
    print(f"Analysis completed successfully. Output saved to '{output_file}'.")
    return output
