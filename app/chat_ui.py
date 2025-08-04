import streamlit as st
import requests

st.title("Conversational AI with RAG")

# Use session state to store the last response
if "chat_response" not in st.session_state:
    st.session_state["chat_response"] = ""

api_url = "http://localhost:8000/chat/"
login_form_url = "https://i.imgur.com/G60h7eK.png"

question = st.text_input("Enter your question:")

def submit_question():
    if question:
        try:
            response = requests.post(api_url, json={"question": question}, timeout=10)
            if response.status_code == 200:
                st.session_state["chat_response"] = response.json().get("response", "No response received.")
            else:
                st.session_state["chat_response"] = f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            st.session_state["chat_response"] = f"Request failed: {e}"
    else:
        st.session_state["chat_response"] = "Please enter a question."

if st.button("Start Chat"):
    submit_question()

if st.session_state["chat_response"]:
    st.markdown(f"**Agent Response:** {st.session_state['chat_response']}")
