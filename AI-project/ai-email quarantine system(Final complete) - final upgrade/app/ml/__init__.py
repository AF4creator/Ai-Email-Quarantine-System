import joblib
import os
from scipy.sparse import hstack
from app.features.url_feature import count_urls

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "spam_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

spam_model = None
tfidf_vectorizer = None


def load_model():
    global spam_model, tfidf_vectorizer

    spam_model = joblib.load(MODEL_PATH)
    tfidf_vectorizer = joblib.load(VECTORIZER_PATH)


def predict_from_text(email_text):
    if spam_model is None:
        load_model()

    text_vec = tfidf_vectorizer.transform([email_text])
    url_count = count_urls(email_text)

    X = hstack([text_vec, [[url_count]]])
    return float(spam_model.predict_proba(X)[0][1])
