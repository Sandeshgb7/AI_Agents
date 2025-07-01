import ollama
import json
from datetime import datetime
import os

ESCALATION_THRESHOLD = 0.6
ESCALATION_LOG = "logs/escalation_log.txt"

def escalate_if_needed(input_json):
    email_text = input_json["email_text"]
    category = input_json["predicted_category"]
    confidence = input_json["confidence"]

    if confidence < ESCALATION_THRESHOLD or category.lower() == "other":
        os.makedirs("logs", exist_ok=True)
        log_entry = f"[{datetime.now()}] Category: {category}, Confidence: {confidence}\nEmail: {email_text}\n\n"

        with open(ESCALATION_LOG, "a", encoding="utf-8") as f:
            f.write(log_entry)

        return {
            "status": "escalated",
            "reason": "Low confidence or unknown category",
            "logged_to": ESCALATION_LOG
        }
    else:
        return {
            "status": "not escalated",
            "reason": "Confidence sufficient and category is specific"
        }

# --- Dynamic prompt template based on category ---
def get_prompt(email_text, category):
    if category == "IT":
        prompt = f"""You are an IT support assistant. Read the following email and generate a helpful, professional reply.

Email: {email_text}

Reply:"""
    elif category == "HR":
        prompt = f"""You are an HR representative. Read the following email and draft a formal, polite response.

Email: {email_text}

Reply:"""
    else:
        prompt = f"""You are a general office assistant. Read the email below and provide an appropriate general response.

Email: {email_text}

Reply:"""
    return prompt

# --- Generate reply using Ollama ---
def generate_reply(input_json, model_name="llama3"):
    email_text = input_json["email_text"]
    category = input_json["predicted_category"]

    prompt = get_prompt(email_text, category)

    response = ollama.chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])

    reply_text = response['message']['content'].strip()

    return {
        "response": reply_text
    }

# --- Example usage ---
if __name__ == "__main__":
    input_json = {
        "email_text": "Hi, I forgot my laptop password. Please help.",
        "predicted_category": "IT"
    }

    result = generate_reply(input_json)
    print(json.dumps(result, indent=4))
