import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Streaming AI Chatbot", page_icon="🤖")
st.header('Powerful Assistant 🤖', divider='rainbow', )

def configure_api_key(api_key):
    try:
        genai.configure(api_key=api_key)
        st.success("API key configured successfully!")
    except Exception as e:
        st.error(f"Error configuring API key: {e}")

# Initial API key setup
api_key = os.getenv('GENAI_API_KEY')
if api_key:
    configure_api_key(api_key)
else:
    st.warning("No API key found in environment. Please enter your API key below.")

api_key_input = st.text_input("Enter your GenAI API key:", type="password")
if api_key_input:
    configure_api_key(api_key_input)

# Model initialization
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_response(user_query, chat_history=""):
    """
    Generates response using Google GenAI

    Args:
        user_query: User's question.
        chat_history: Optional conversation history string.

    Returns:
        The AI's response to the user's query.
    """
    try:
        prompt = f"You are a helpful assistant. Answer the following question considering the history of the conversation:\n {chat_history}\n User question: {user_query}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history])
    response = get_response(user_query, chat_history)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
