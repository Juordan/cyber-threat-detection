import re
import ipaddress
from urllib.parse import urlparse

def extract_url_features(url):

    url = str(url)

    # Mengubah URL menjadi format yang dapat dibaca urlparse
    # Jika belum memiliki skema, tambahkan skema sementara
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url):
        url_to_parse = 'http://' + url
    else:
        url_to_parse = url

    try:
        parsed = urlparse(url_to_parse)

        hostname = parsed.hostname or ''
        path = parsed.path or ''
        query = parsed.query or ''

    except Exception:
        hostname = ''
        path = ''
        query = ''

        parsed = None

    # Menghitung jumlah subdomain secara sederhana
    domain_parts = hostname.split('.') if hostname else []

    subdomain_count = max(len(domain_parts) - 2, 0)

    # Memeriksa apakah hostname berupa alamat IP
    try:
        ipaddress.ip_address(hostname)
        has_ip_address = 1
    except ValueError:
        has_ip_address = 0

    # Mengubah URL menjadi lowercase hanya untuk pencarian keyword
    url_lower = url.lower()

    # Daftar keyword yang akan diperiksa
    suspicious_keywords = [
        'login',
        'verify',
        'account',
        'secure',
        'update',
        'signin',
        'password',
        'banking',
        'confirm',
        'wallet'
    ]

    # Ekstraksi fitur numerik
    features = {
        'url_length': len(url),
        'domain_length': len(hostname),
        'path_length': len(path),
        'query_length': len(query),

        'count_dot': url.count('.'),
        'count_hyphen': url.count('-'),
        'count_at': url.count('@'),
        'count_question': url.count('?'),
        'count_equal': url.count('='),
        'count_slash': url.count('/'),
        'count_percent': url.count('%'),
        'count_ampersand': url.count('&'),
        'count_underscore': url.count('_'),
        'count_digits': sum(char.isdigit() for char in url),

        'subdomain_count': subdomain_count,
        'has_ip_address': has_ip_address,

        'has_https': int(
            parsed is not None and parsed.scheme.lower() == 'https'
        )
    }

    # Ekstraksi fitur keyword
    for keyword in suspicious_keywords:
        features[f'keyword_{keyword}'] = int(
            keyword in url_lower
        )

    return features
