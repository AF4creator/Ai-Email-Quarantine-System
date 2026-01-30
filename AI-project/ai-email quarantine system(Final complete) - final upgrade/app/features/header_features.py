def extract_header_features(headers):
    return {
        "spf_pass": "spf=pass" in headers.lower(),
        "dkim_pass": "dkim=pass" in headers.lower()
    }
