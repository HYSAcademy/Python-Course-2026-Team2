import json
import os
import argparse
from analyzer import read_file, get_modified_data, get_statistics
from formatter import format_data


def validate_input_file(input_file: str) -> bool:
    """Перевіряє, чи існує файл, чи це TXT та чи він не порожній."""
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
    """Повертає шлях до output JSON файлу."""
    if output_arg:
        return f"{output_arg}.json" if not output_arg.endswith(".json") else output_arg
    return f"{os.path.splitext(input_file)[0]}.analysis.json"


def run_cli():
    """
    CLI для Mini Document Analyzer.

    Використання:
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
    content = read_file(input_file)
    data = get_modified_data(content)
    statistics = get_statistics(data['tokens'], content)
    output = format_data(input_file, data, statistics)

   
    print(f"Analysis completed successfully. Output saved to '{output_file}'.")
    return output

