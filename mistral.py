#!/usr/bin/env python3

import argparse
import os
import subprocess
import requests
import json
from urllib.parse import urlparse

def get_api_key():
    """Retrieve the API key from environment variables."""
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set MISTRAL_API_KEY.")
    return api_key

def get_headers(url):
    """Fetch HTTP headers for the given URL."""
    try:
        response = requests.head(url, allow_redirects=True)
        return dict(response.headers)
    except requests.RequestException as e:
        print(f"Error fetching headers: {e}")
        return {"Header": "Error fetching headers."}

def get_mistral_extensions(url, headers, api_key, max_extensions):
    """Request Mistral API for likely file extensions based on URL and headers."""
    endpoint = "https://api.mistral.ai/v1/chat/completions"
    
    # Create the prompt for Mistral API
    prompt = f"""
    Given the following URL and HTTP headers, suggest the most likely file extensions for fuzzing this endpoint.
    Respond with a JSON object containing a list of extensions in the format: {{"extensions": [".ext1", ".ext2", ...]}}.
    Do not suggest more than {max_extensions}, and only suggest extensions that make sense.

    URL: {url}
    Headers: {headers}

    JSON Response:
    """

    # Prepare headers and payload for Mistral API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",
        "temperature": 0.3,
        "top_p": 1,
        "max_tokens": 1000,
        "stream": False,
        "stop": ["\n\n"],  # Stop generation at double new lines
        "random_seed": 0,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "text"},
        "tools": [],
        "tool_choice": "auto",
        "safe_prompt": False
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        # print("Response Content:", response_data)

        if 'choices' in response_data and len(response_data['choices']) > 0:
            # Extract the assistant's response
            assistant_response = response_data['choices'][0]['message']['content']
            # Remove the Markdown formatting
            assistant_response = assistant_response.strip('```json\n').strip('```').strip()
            # Parse the JSON response
            extensions_data = json.loads(assistant_response)
            return extensions_data
        else:
            print("Error: Received an unexpected response structure from the Mistral API.")
            return {"extensions": []}

    except requests.exceptions.HTTPError as err:
        print(f"Error with Mistral API request: {err}")
        return {"extensions": []}
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}. Assistant response was: {assistant_response}")
        return {"extensions": []}


def main():
    parser = argparse.ArgumentParser(description='AI-powered fuzzing extension suggestion tool')
    parser.add_argument('--max-extensions', type=int, default=5, help='Maximum number of extensions to suggest')
    args, unknown = parser.parse_known_args()

    # Find the -u argument in the unknown args
    try:
        url_index = unknown.index('-u') + 1
        url = unknown[url_index]
    except (ValueError, IndexError):
        print("Error: -u URL argument is required.")
        return

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')

    if 'FUZZ' not in path_parts[-1]:
        print("Warning: FUZZ keyword is not at the end of the URL path. Extension fuzzing may not work as expected.")

    base_url = url.replace('FUZZ', '')
    headers = get_headers(base_url)

    api_key = get_api_key()
    
    extensions_data = get_mistral_extensions(url, headers, api_key, args.max_extensions)
    extensions = ','.join(extensions_data.get('extensions', [])[:args.max_extensions])
    
    ffuf_command = ['ffuf'] + unknown + ['-e', extensions]

    subprocess.run(ffuf_command)

if __name__ == '__main__':
    main()


# usage
# python  mistral.py --max-extensions 6 -u https://github.com/FUZZ -w ~/wordlist/Bug-Bounty-Wordlists/config.txt