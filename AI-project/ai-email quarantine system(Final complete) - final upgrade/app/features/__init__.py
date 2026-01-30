from .header_features import extract_header_features
from .text_feature import extract_text_features

def extract_all_features(
    text: str,
    headers: str = "",
    urls: dict | None = None,
    vectorizer=None
):
    """
    Extract all features for ML model.
    """
    header_feats = extract_header_features(headers)

    # 🔴 URLs are already processed in pipeline
    url_feats = urls or {}

    text_vector = extract_text_features(text, vectorizer)

    return {
        "header": header_feats,
        "url": url_feats,
        "text_vector": text_vector
    }
