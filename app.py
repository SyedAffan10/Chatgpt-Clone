import os
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="ChatGPT Clone", layout="wide")
st.title("ChatGPT Clone")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**ChatGPT:** {message['content']}")

# Divider to keep input field at the bottom
st.write("---")

# Input and file upload form
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message here...", key="chat_input")
        submitted = st.form_submit_button("Send")

# Handle form submission
if submitted:
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content

        # Append assistant's reply
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        error_message = f"Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})

    # Refresh the chat display
    st.rerun()
