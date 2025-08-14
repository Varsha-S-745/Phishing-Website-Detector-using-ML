import re
import urllib.parse

def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(url.count('@'))
    features.append(1 if url.startswith("https") else 0)
    features.append(sum(c.isdigit() for c in url))
    features.append(url.count('-'))
    domain = urllib.parse.urlparse(url).netloc
    features.append(len(domain))
    return features
