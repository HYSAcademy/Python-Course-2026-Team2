import json
import os
import argparse
from analyzer import read_file, get_modified_data, get_statistics
from formatter import format_data


def get_output_file(input_file: str, output_arg: str | None) -> str:
    """Повертає шлях до output JSON файлу."""
    if output_arg:
        return output_arg
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


    # --- ANALYSIS PIPELINE ---
    content = read_file(input_file)
    data = get_modified_data(content)
    statistics = get_statistics(data['tokens'], content)
    output = format_data(input_file, data, statistics)

    
    print(f"Analysis completed successfully. Output saved to '{output_file}'.")
    return output

