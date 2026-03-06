import json
import os


def export_to_json(output_data, output_file):
    """
    Save the output data to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

def run_cli():

    """
    Expect exactly 1 or 2 arguments after the script name.
    The first argument is the required input file path, and the second
    (optional) argument is the desired output file name.
    """
    parser = argparse.ArgumentParser(
        description="Analyze a TXT file and export results to JSON"
    )
    parser.add_argument(
        "input_file",
        type=validate_input_file,
        help="Path to the input TXT file"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="Optional output JSON file name"
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file or f"{os.path.splitext(input_file)[0]}.analytics.json"
