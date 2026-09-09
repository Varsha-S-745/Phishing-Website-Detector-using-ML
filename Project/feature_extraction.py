import re
import urllib.parse
from ipaddress import ip_address

def is_ip(domain):
    try:
        ip_address(domain)
        return 1
    except ValueError:
        return 0


def extract_features(url):
    try:
        parsed = urllib.parse.urlparse(url)

        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        query = parsed.query.lower()

        suspicious_words = [
            "login",
            "verify",
            "secure",
            "account",
            "update",
            "bank",
            "paypal",
            "signin",
            "confirm",
            "password"
        ]

        features = [
            len(url),
            len(domain),
            url.count("."),
            url.count("-"),
            sum(c.isdigit() for c in url),
            url.count("@"),
            url.count("?"),
            url.count("="),
            url.count("%"),
            url.count("//"),
            1 if parsed.scheme == "https" else 0,
            is_ip(domain),
            max(0, len(domain.split(".")) - 2),
            len(urllib.parse.parse_qs(query)),
            sum(
                1
                for word in suspicious_words
                if word in url.lower()
            ),
            len(path),
            len(re.findall(r'[^A-Za-z0-9]', url))

        ]

        return features

    except Exception:
        return [0] * 17
