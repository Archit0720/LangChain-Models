import requests
import streamlit as st

# 🔁 GROQ-based essay generation
def get_groq_response(input_text):
    response = requests.post(
        "http://localhost:8000/essay/invoke",
        json={'input': {'topic': input_text}}
    )

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        try:
            # Attempt to extract the 'output' from the response
            return response.json().get('output', "❌ No output in the response")
        except ValueError:
            # Handle the case where JSON decoding fails
            return "❌ Error: Unable to parse JSON from response"
    else:
        # Return the status code and raw response content if error occurs
        return f"❌ Error: Status code {response.status_code}, Response: {response.text}"

# 🦙 Ollama-based poem generation
def get_ollama_response(input_text):
    response = requests.post(
        "http://localhost:8000/poem/invoke",
        json={'input': {'topic': input_text}}
    )

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        try:
            # Attempt to extract the 'output' from the response
            return response.json().get('output', "❌ No output in the response")
        except ValueError:
            # Handle the case where JSON decoding fails
            return "❌ Error: Unable to parse JSON from response"
    else:
        # Return the status code and raw response content if error occurs
        return f"❌ Error: Status code {response.status_code}, Response: {response.text}"

# 🎨 Streamlit UI
st.title('Langchain Demo with Groq & LLAMA2')

# Input fields
input_text = st.text_input("Enter a topic for the essay (Groq)")
input_text1 = st.text_input("Enter a topic for the poem (LLAMA2 via Ollama)")

# Display essay result from Groq
if input_text:
    st.subheader("Essay (via Groq):")
    st.write(get_groq_response(input_text))

# Display poem result from Ollama
if input_text1:
    st.subheader("Poem (via LLAMA2):")
    st.write(get_ollama_response(input_text1))
