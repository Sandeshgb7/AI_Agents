import numpy as np
import joblib
import json
from gensim.models import FastText
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
import re
#C:\Users\sandesh badiger\Desktop\Documents\smart-email-assistant\orchestrator.py
# --- Load model and FastText ---
model_path = r"C:\\Users\\sandesh badiger\\Desktop\\Documents\\smart-email-assistant\\models\\classification_model.pkl"
fasttext_path = r"C:\\Users\\sandesh badiger\\Desktop\\Documents\\smart-email-assistant\\models\\fasttext_model.model"

classifier = joblib.load(model_path)
fasttext_model = FastText.load(fasttext_path)

# --- Text preprocessing ---
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    review = re.sub(r'[^a-zA-Z\s]', ' ', text).lower()
    tokens = review.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def avg_fasttext(words, model):
    valid_vectors = [model.wv[word] for word in words if word in model.wv.index_to_key]
    if valid_vectors:
        return np.mean(valid_vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

# --- Predict function ---
def classify_email(email_json):
    email_text = email_json["email_text"]
    tokens = preprocess(email_text)
    vector = avg_fasttext(tokens, fasttext_model).reshape(1, -1)

    predicted_label = classifier.predict(vector)[0]
    probs = classifier.predict_proba(vector)
    confidence = np.max(probs)

    return {
        "email_text": email_text,
        "predicted_category": predicted_label,
        "confidence": round(float(confidence), 2)
    }

if __name__ == "__main__":
    email = "Hi, I forgot my laptop password. Please help."
    output = orchestrate_email(email)
    import json
    print(json.dumps(output, indent=4))
