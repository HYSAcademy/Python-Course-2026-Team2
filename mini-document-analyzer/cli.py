import json
import sys
import os


def run_cli():

    # Expect exactly 1 or 2 arguments after the script name.
    # The first argument is the required input file path, and the second
    # (optional) argument is the desired output file name.
    if len(sys.argv) < 2:
        print("Error: Missing input file argument")
        sys.exit(1)
    if len(sys.argv) > 3:
        print("Error: Too many arguments")
        print("Usage: python -m mini_document_analyzer.cli <input.txt> [output.json]")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file) or not input_file.endswith('.txt'):
        print("Error: Input file must be a valid TXT file")
        sys.exit(1)
        
    if os.stat(input_file).st_size == 0:
        print(f"Error: {input_file} is empty")
        sys.exit(1)
        
    if len(sys.argv) == 3 and sys.argv[2].endswith('.json'):
        output_file = sys.argv[2]
    else:
        output_file = f"{os.path.splitext(input_file)[0]}.analytics.json"
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")


# Call the main analysis function from the core module and write results to output file.


