# chatbot-with-langgraph-streamlit]
This project is an LLM-powered chatbot built with LangGraph and LangChain, integrating a HuggingFace model (Mistral-7B), persistent SQLite storage, thread/chat session naming, rich observability via LangSmith, and a modern Streamlit-based interface.

✨ Features
Conversational LLM: Uses Mistral-7B via HuggingFace, with chat context retention.
Multi-threaded chat: Unique conversations with thread IDs, management, and naming.
Persistent history: Messages and metadata stored in SQLite.
Observability with LangSmith: Track, visualize, and debug all LLM interactions and conversations.
Modern Streamlit frontend:
View all chat threads, select sessions, rename chats

Real-time chat interface
History retrieval

🚀 Quickstart Instructions
1. Clone and set up the repo
   
2. git clone <repo-url>
cd <repo-folder>
3. Install dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Copy .env.example → .env

Add your HuggingFace and LangSmith API credentials:

HUGGINGFACEHUB_API_TOKEN=your-hf-token
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
5. Run the Streamlit UI

streamlit run app.py
(Change app.py to your Streamlit UI file.)

6. Start chatting!

Each chat is saved to a thread.

All interactions are observable in your LangSmith dashboard.

