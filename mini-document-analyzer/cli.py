import json
import os
from analyzer import read_file, get_modified_data, get_statistics
from formatter import format_data

content = read_file('path.txt') # Change to input file path
data = get_modified_data(content)
statistics = get_statistics(data['tokens'], content)
output = format_data('path.txt', data, statistics) # Change to input file path


def run_cli():