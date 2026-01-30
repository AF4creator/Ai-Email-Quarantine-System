import re

URL_REGEX = r'https?://[^\s]+|www\.[^\s]+'

def extract_urls(text: str):
    if not text:
        return []
    return re.findall(URL_REGEX, text)

def count_urls(text: str) -> int:
    return len(extract_urls(text))

def check_urls(urls):
    suspicious = any(
        "bit.ly" in url or "tinyurl" in url
        for url in urls
    )
    return {"suspicious_url": suspicious}
