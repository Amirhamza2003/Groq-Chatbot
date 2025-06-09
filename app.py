import streamlit as st
from groq import Groq
import json
import os

# Inject custom CSS for dark theme, blue borders, and fancy input area
st.markdown("""
    <style>
    body, .stApp {
        background-color: #181c24 !important;
        color: #e0e6ed !important;
    }
    .main {
        background-color: #181c24 !important;
    }
    .chat-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #4fc3f7;
        margin-bottom: 2rem;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px #0008;
        text-align: center;
        padding-top: 2rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #232a36;
        background: linear-gradient(90deg, #181c24 60%, #232a36 100%);
    }
    .chat-title .icon {
        font-size: 2.2rem;
        vertical-align: middle;
        margin-right: 0.5rem;
    }
    .chat-bubble {
        border: 2px solid #2196f3;
        border-radius: 18px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.2rem;
        background: #232a36;
        color: #e0e6ed;
        font-size: 1.1rem;
        box-shadow: 0 2px 12px #0004;
        max-width: 80%;
        word-break: break-word;
    }
    .user-bubble {
        margin-left: auto;
        border-color: #4fc3f7;
        background: #1a2233;
    }
    .assistant-bubble {
        margin-right: auto;
        border-color: #2196f3;
        background: #232a36;
    }
    section[data-testid="stChatInput"] {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #181c24 !important;
        padding: 2rem 0 3rem 0;
    }
    section[data-testid="stChatInput"] > div {
        width: 60vw !important;
        min-width: 320px;
        max-width: 700px;
        margin: 0 auto;
        background: #232a36 !important;
        border: 2px solid #2196f3 !important;
        border-radius: 2rem !important;
        box-shadow: 0 2px 16px #0006;
        padding: 0.5rem 1.5rem;
        display: flex;
        align-items: center;
    }
    section[data-testid="stChatInput"] input, 
    section[data-testid="stChatInput"] textarea {
        background: #232a36 !important;
        color: #e0e6ed !important;
        border: none !important;
        font-size: 1.1rem !important;
        padding: 1rem 0.5rem !important;
        box-shadow: none !important;
        border-radius: 2rem !important;
    }
    section[data-testid="stChatInput"] input:focus, 
    section[data-testid="stChatInput"] textarea:focus {
        outline: 2px solid #2196f3 !important;
        background: #232a36 !important;
    }
    section[data-testid="stChatInput"] input::placeholder, 
    section[data-testid="stChatInput"] textarea::placeholder {
        color: #b0b8c1 !important;
        opacity: 1 !important;
    }
    section[data-testid="stChatInput"] button {
        background: #2196f3 !important;
        color: #fff !important;
        border-radius: 50% !important;
        width: 2.5rem !important;
        height: 2.5rem !important;
        font-size: 1.3rem !important;
        margin-left: 0.5rem;
        transition: background 0.2s;
        border: none !important;
    }
    section[data-testid="stChatInput"] button:hover {
        background: #1769aa !important;
    }
    /* Remove red border on focus/error */
    section[data-testid="stChatInput"] input:focus, 
    section[data-testid="stChatInput"] input:active, 
    section[data-testid="stChatInput"] input:focus-visible {
        border: none !important;
        box-shadow: 0 0 0 2px #2196f3 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Groq API details
GROQ_API_KEY = "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"
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

client = Groq(api_key=GROQ_API_KEY)

# Load chat history from file
def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            return json.load(f)
    return []

# Save chat history to file
def save_chat_history(messages):
    with open("chat_history.json", "w") as f:
        json.dump(messages, f)

st.markdown('<div class="chat-title"><span class="icon"></span>Groq Chatbot</div>', unsafe_allow_html=True)

# Initialize session state with chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# User input
prompt = st.chat_input("Type your message and press Enter...")

# If user just sent a message, process it immediately
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Groq is thinking..."):
        completion = client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_chat_history(st.session_state.messages)

# Display chat history with custom bubbles
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-bubble user-bubble">🧑‍💻 {msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble assistant-bubble">🤖 {msg["content"]}</div>',
            unsafe_allow_html=True
        )

if st.button("Clear Chat History"):
    st.session_state.messages = []
    save_chat_history(st.session_state.messages)
    st.rerun()
