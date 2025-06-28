import ollama

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
        prompt = f"""You are a general support assistant. Please read this email and generate a polite and relevant reply.

Email: {email_text}

Reply:"""
    return prompt

def generate_reply(input_data, model_name="llama3"):
    category = input_data.get("predicted_category")
    email_text = input_data.get("email_text")

    prompt = get_prompt(email_text, category)

    try:
        response = ollama.chat(model=model_name, messages=[
            {"role": "user", "content": prompt}
        ])

        reply = response['message']['content'].strip()
        return {"response": reply}
    
    except Exception as e:
        return {
            "response": "❌ Failed to generate response using Ollama.",
            "error": str(e)
        }

# Example test
if __name__ == "__main__":
    input_json = {
        "email_text": "Hi, I forgot my laptop password. Please help.",
        "predicted_category": "IT"
    }

    result = generate_reply(input_json)
    import json
    print(json.dumps(result, indent=4))
