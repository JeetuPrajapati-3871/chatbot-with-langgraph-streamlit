import streamlit as st
from chatbot_backend import chatbot, all_threads, save_thread, save_message, load_messages, get_all_threads,llm
from langchain_core.messages import HumanMessage
from langchain_huggingface import ChatHuggingFace
import uuid
import sqlite3

# =================== LLM Setup for Chat Title ===================


def generate_chat_name(first_message: str) -> str:
    """Use LLM to generate a short, meaningful chat title."""
    prompt = f"""
    Generate a short (max 5 words) chat title for this message:
    "{first_message}"
    Return only the title text.
    """
    try:
        result = llm.invoke(prompt)
        return result.content.strip().replace('"', '')
    except Exception:
        return "New Chat"

# =================== Utility Functions ===================
def get_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state['thread_id'] = get_thread_id()
    st.session_state['message_history'] = []
    st.session_state['chat_name'] = None

# =================== Streamlit Session Setup ===================
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = get_thread_id()
if 'chat_name' not in st.session_state:
    st.session_state['chat_name'] = None

# =================== Sidebar UI ===================
st.sidebar.title('💬 Chatbot')

if st.sidebar.button('➕ New Chat'):
    reset_chat()

st.sidebar.header('📜 My Conversations')

# Fetch threads from backend DB
try:
    all_db_threads = get_all_threads()
except sqlite3.OperationalError:
    all_db_threads = []

# Display threads with chat names
for tid, cname in all_db_threads:
    if st.sidebar.button(f"{cname}", key=f"thread_btn_{tid}"):
        st.session_state['thread_id'] = tid
        st.session_state['chat_name'] = cname
        st.session_state['message_history'] = load_messages(tid)

# =================== Main UI ===================
# Display chat messages
for message in st.session_state['message_history']:
    role = message["role"]
    with st.chat_message(role):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # ✅ Generate chat title if first message
    if not st.session_state.get('chat_name'):
        chat_name = generate_chat_name(user_input)
        st.session_state['chat_name'] = chat_name
        save_thread(st.session_state['thread_id'], chat_name)

    # ✅ Show user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    save_message(st.session_state['thread_id'], "user", user_input)
    with st.chat_message('user'):
        st.markdown(user_input)

    # ✅ LangGraph config
    CONFIG = {
        'configurable': {'thread_id': st.session_state['thread_id']},
        "run_name": "my_chatbot",
        "metadata": {"thread_id": st.session_state['thread_id']}
    }

    # ✅ Get response from chatbot (streamed)
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    # ✅ Save bot response
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    save_message(st.session_state['thread_id'], "bot", ai_message)
