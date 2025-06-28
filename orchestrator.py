import json
from agents.email_classifier import classify_email
from agents.response_generator import generate_reply
from agents.escalation_agent import escalate_if_needed

def orchestrate_email(email_text):
    classification_output = classify_email({"email_text": email_text})
    category = classification_output["predicted_category"]
    confidence = classification_output["confidence"]

    if confidence < 0.6 or category.lower() == "other":
        escalation_output = escalate_if_needed({
            "email_text": email_text,
            "predicted_category": category,
            "confidence": confidence
        })
        return {
            "email_text": email_text,
            "predicted_category": category,
            "confidence": confidence,
            "result": escalation_output
        }

    llm_output = generate_reply({
        "email_text": email_text,
        "predicted_category": category
    })

    return {
        "email_text": email_text,
        "predicted_category": category,
        "confidence": confidence,
        "result": llm_output
    }
