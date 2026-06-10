import google.generativeai as genai
import streamlit as st


genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def get_ai_response(messages):

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

    conversation = ""

    for msg in messages:

        role = msg["role"]

        if role == "user":
            conversation += f"User: {msg['content']}\n"

        else:
            conversation += f"Assistant: {msg['content']}\n"

    response = model.generate_content(
        conversation
    )

    return response.text