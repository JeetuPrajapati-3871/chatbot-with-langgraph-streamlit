from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    max_new_tokens=120
)
llm=ChatHuggingFace(llm=llm)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

conn = sqlite3.connect(database='my_chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# def all_threads():
#     all_threads = set()
#     for checkpoint in checkpointer.list(None):
#         all_threads.add(checkpoint.config['configurable']['thread_id'])

#     return list(all_threads)
def all_threads():
    """Return unique thread IDs from the checkpointer."""
    threads_set = set()
    for checkpoint in checkpointer.list(None):
        # checkpoint[0] is the config dictionary
        config = checkpoint[0] if len(checkpoint) > 0 else {}
        thread_id = config.get('configurable', {}).get('thread_id')
        if thread_id:
            threads_set.add(thread_id)
    # return sorted list for consistent order
    return sorted(list(threads_set))



# ========================= Thread Management (for Frontend) ==========================
def init_thread_tables():
    """Create tables for storing chat titles and messages."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threads (
            thread_id TEXT PRIMARY KEY,
            chat_name TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()

def save_thread(thread_id, chat_name):
    """Insert or update thread metadata."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO threads (thread_id, chat_name, created_at)
        VALUES (?, ?, datetime('now'))
    """, (thread_id, chat_name))
    conn.commit()

def save_message(thread_id, sender, message):
    """Save individual user/bot messages for the frontend view."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (thread_id, sender, message, timestamp)
        VALUES (?, ?, ?, datetime('now'))
    """, (thread_id, sender, message))
    conn.commit()


def load_messages(thread_id):
    """Retrieve messages from the messages table."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, message FROM messages WHERE thread_id=? ORDER BY id
    """, (thread_id,))
    rows = cursor.fetchall()
    return [{"role": "user" if s == "user" else "assistant", "content": m} for s, m in rows]

def get_all_threads():
    """Return all thread IDs and chat names."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT thread_id, chat_name FROM threads ORDER BY created_at DESC
    """)
    return cursor.fetchall()

# Initialize tables on import
init_thread_tables()


