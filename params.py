import sys
from urllib.parse import urlparse, parse_qs

def extract_param_keys():
    # Read input from stdin
    input_url = sys.stdin.read().strip()  # Read the entire input and strip whitespace

    # Parse the URL
    parsed_url = urlparse(input_url)
    
    # Parse the query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the keys from the query parameters
    keys = list(query_params.keys())

    # Print each key
    for key in keys:
        print(key)

if __name__ == "__main__":
    extract_param_keys()
