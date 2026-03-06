import json
import sys
import os
import argparse


def run_cli():

    # Expect exactly 1 or 2 arguments after the script name.
    # The first argument is the required input file path, and the second
    # (optional) argument is the desired output file name.
    
    parser = argparse.ArgumentParser(description="Mini Document Analyzer")

    parser.add_argument(
        "input",
        help="Path to input TXT file"
    )

    parser.add_argument(
        "output",
        nargs="?",  # optional positional argument
        help="Optional output JSON filename"
    )

    args = parser.parse_args()

    input_file = args.input

    if not os.path.isfile(input_file) or not input_file.endswith(".txt"):
        print("Error: Input file must be a valid TXT file")
        return

    if os.stat(input_file).st_size == 0:
        print(f"Error: {input_file} is empty")
        return

    if args.output:
        output_file = args.output
    else:
        output_file = f"{os.path.splitext(input_file)[0]}.analysis.json"

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
     # --- ANALYSIS PIPELINE ---
     


    # --- JSON EXPORT ---
        
    export_json(output, output_file)
    print("Analysis completed successfully.")


def export_json(data,output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)


