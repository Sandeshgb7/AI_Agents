import streamlit as st
from orchestrator import orchestrate_email
import json

st.set_page_config(page_title="📧 Smart Email Assistant", layout="centered")

st.title("📨 Smart Email Assistant")
st.write("Enter a company email. The system will classify it, respond, or escalate it.")

email_text = st.text_area("✉️ Enter Email Text", height=200)

if st.button("🔍 Run Smart Agent"):
    if not email_text.strip():
        st.warning("Please enter some email text.")
    else:
        result = orchestrate_email(email_text)
        st.subheader("📋 Result")
        st.json(result)
