def extract_text_features(text, vectorizer):
    """
    Transform text into TF-IDF vector using the given vectorizer.
    """
    if vectorizer is None:
        raise ValueError("TF-IDF vectorizer is None!")
    return vectorizer.transform([text])
