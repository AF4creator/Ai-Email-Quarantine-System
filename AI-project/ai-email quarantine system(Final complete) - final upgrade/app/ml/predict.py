import os
import pickle
from scipy.sparse import hstack
from app.features import extract_all_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VEC_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "spam_model.pkl")

# Globals (start empty on purpose)
_tfidf_vectorizer = None
_spam_model = None


def _load_models():
    global _tfidf_vectorizer, _spam_model

    if _tfidf_vectorizer is None:
        if not os.path.exists(VEC_PATH):
            raise FileNotFoundError(f"TF-IDF vectorizer not found: {VEC_PATH}")
        with open(VEC_PATH, "rb") as f:
            _tfidf_vectorizer = pickle.load(f)

    if _spam_model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Spam model not found: {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as f:
            _spam_model = pickle.load(f)


def predict_spam(email_text, email_headers="", urls_list=None):
    """
    Predict spam probability (0.0 – 1.0)
    """
    _load_models()

    features = extract_all_features(
        text=email_text,
        headers=email_headers,
        urls=urls_list,
        vectorizer=_tfidf_vectorizer
    )

    text_vector = features["text_vector"]
    url_feat = features["url"]

    url_feature = [[1 if url_feat.get("suspicious_url") else 0]]

    X = hstack([text_vector, url_feature])

    prob = _spam_model.predict_proba(X)[0][1]
    return round(float(prob), 2)
