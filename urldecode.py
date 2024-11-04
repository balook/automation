import sys
import urllib.parse

def url_decode(encoded_url):
    decoded_url = urllib.parse.unquote(encoded_url)
    return decoded_url

if __name__ == "__main__":
    # Read URL-encoded string from standard input (pipe)
    encoded_url = sys.stdin.read().strip()
    
    # Decode the URL
    decoded_url = url_decode(encoded_url)
    
    # Print the decoded URL without any extra text
    print(decoded_url)
