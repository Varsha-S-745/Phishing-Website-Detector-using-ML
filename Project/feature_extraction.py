import re
import urllib.parse

def extract_features(url):
    features = []
    # Length of URL
    features.append(len(url))
    # Count of '.'
    features.append(url.count('.'))
    # Count of '@'
    features.append(url.count('@'))
    # Check for HTTPS
    features.append(1 if url.startswith("https") else 0)
    # Count of digits
    features.append(sum(c.isdigit() for c in url))
    # Presence of '-'
    features.append(url.count('-'))
    # Length of domain
    domain = urllib.parse.urlparse(url).netloc
    features.append(len(domain))
    return features
