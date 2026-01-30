import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "..", "ml", "spam_model.pkl")
VECT_PATH = os.path.join(BASE_DIR, "..", "..", "ml", "tfidf_vectorizer.pkl")

with open(MODEL_PATH, "rb") as f:
    spam_model = pickle.load(f)

with open(VECT_PATH, "rb") as f:
    tfidf_vectorizer = pickle.load(f)
