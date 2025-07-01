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

