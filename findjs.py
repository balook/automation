import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_js_files(url):
    try:
        # Fetch the HTML content of the page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all script tags and extract the src attribute
        js_files = []
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                # Resolve relative URLs
                js_files.append(urljoin(url, src))

        return js_files
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

if __name__ == "__main__":
    # Read hostname from standard input (pipe)
    for hostname in sys.stdin:
        hostname = hostname.strip()  # Remove any extra whitespace or newline
        if hostname:  # Check if the line is not empty
            # Add 'http://' if the input does not start with 'http://' or 'https://'
            if not hostname.startswith(('http://', 'https://')):
                hostname = 'http://' + hostname
            
            # Find JavaScript files
            js_files = find_js_files(hostname)
            
            # Print the found JavaScript files
            for js_file in js_files:
                print(js_file)
