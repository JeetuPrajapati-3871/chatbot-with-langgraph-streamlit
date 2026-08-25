 LLM Chatbot with LangGraph, RAG & Streamlit

An LLM-powered conversational chatbot built with LangGraph, LangChain, Hugging Face Mistral-7B, RAG, SQLite, FAISS, and Streamlit.

The project started as a Streamlit-based chatbot and was extended with persistent multi-threaded conversations and a RAG pipeline for answering domain-specific questions that the base LLM may not reliably know.

✨ Features

🧠 Mistral-7B-Instruct-v0.3 as the base LLM through Hugging Face

🔄 LangGraph for managing the chatbot execution flow

💬 Multi-threaded conversations with unique thread IDs

💾 Persistent chat history using SQLite

🏷️ Chat/thread management with conversation names and metadata

🔍 RAG architecture for domain-specific knowledge retrieval

📚 PDF document ingestion for knowledge-base creation

🧩 Text chunking and embeddings using Hugging Face

🗂️ FAISS vector database for similarity search

🎯 RetrievalQA for combining retrieved context with the LLM

🚫 Context-grounded responses so the RAG assistant can indicate when information is unavailable

📊 LangSmith observability for tracing and debugging LLM interactions

🎨 Streamlit UI for the current chatbot interface

🏗️ Architecture

Chatbot Architecture

                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Chat / Thread     │
                    │     Management      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      LangGraph      │
                    │    StateGraph       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Mistral-7B LLM    │
                    │   Hugging Face      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ SQLite Checkpointer │
                    │ + Chat Metadata     │
                    └─────────────────────┘

RAG Architecture

             Documents / PDF
                    │
                    ▼
             Document Loader
                    │
                    ▼
             Text Splitting
                    │
                    ▼
          Hugging Face Embeddings
                    │
                    ▼
              FAISS Vector DB
                    │
                    ▼
               Retriever
                    │
              Top-k Context
                    │
                    ▼
              Prompt + Context
                    │
                    ▼
              Mistral-7B LLM
                    │
                    ▼
                 Answer

The RAG pipeline loads documents, splits them into chunks, creates embeddings, stores them in FAISS, retrieves relevant chunks, and passes the retrieved context to the LLM.

🧠 RAG Knowledge Base

The project includes a RAG implementation for a customer-support use case.

Example knowledge source:

Flipkart Policies / Customer Support Documentation

The current RAG pipeline uses:

PyPDFLoader for PDF ingestion

CharacterTextSplitter for chunking

all-MiniLM-L6-v2 for embeddings

FAISS for vector storage

Similarity retrieval with top-k documents

RetrievalQA to combine retrieved context with Mistral-7B

The prompt instructs the system to avoid inventing policy information when the answer is not present in the retrieved context.

🧵 Multi-Threaded Chat System

Every conversation is associated with a unique thread_id.

The system maintains:

Thread
 ├── thread_id
 ├── chat_name
 └── created_at

Messages
 ├── id
 ├── thread_id
 ├── sender
 ├── message
 └── timestamp

This allows users to:

Create separate conversations

Switch between previous chats

Preserve conversation history

Rename conversations

Continue an existing conversation

LangGraph's SQLite checkpointer is also used to persist graph state across threads.

🛠️ Tech Stack

Layer

Technology

LLM

Mistral-7B-Instruct-v0.3

LLM Provider

Hugging Face

LLM Framework

LangChain

Agent / Workflow Framework

LangGraph

RAG

LangChain RetrievalQA

Embeddings

Hugging Face / MiniLM

Vector Database

FAISS

Current Database

SQLite

Frontend

Streamlit

Observability

LangSmith

Language

Python

Document Source

PDF

📂 Project Structure

chatbot-with-langgraph-streamlit/
│
├── app.py
├── chatbot_backend.py
├── rag_architecture.py
│
├── my_chatbot.db
├── my_chatbot.db-shm
├── my_chatbot.db-wal
│
├── requirements.txt
└── README.md

Main Components

chatbot_backend.py

Contains the LangGraph chatbot, Mistral-7B integration, SQLite checkpointer, thread management, and message persistence.

rag_architecture.py

Contains the RAG pipeline including PDF loading, chunking, embeddings, FAISS vector storage, retrieval, prompting, and RetrievalQA.

app.py

Streamlit frontend for interacting with the chatbot.

🚀 Getting Started

1. Clone the repository

git clone <repo-url>
cd chatbot-with-langgraph-streamlit

2. Install dependencies

pip install -r requirements.txt

3. Configure environment variables

Create a .env file:

HUGGINGFACEHUB_API_TOKEN=your-huggingface-token

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key

4. Run the Streamlit application

streamlit run app.py

Open the local Streamlit URL and start chatting.

🔎 Example RAG Flow

A user asks:

What is the return policy for electronic items?

Instead of relying only on Mistral-7B's pretrained knowledge:

User Question
      ↓
Create Query Embedding
      ↓
Search FAISS
      ↓
Retrieve Relevant Policy Chunks
      ↓
Add Retrieved Context to Prompt
      ↓
Mistral-7B
      ↓
Grounded Answer

This makes the chatbot suitable for knowledge-base and customer-support applications where answers should come from a controlled document collection.

🔮 Future Enhancements

The current project is a strong prototype. The next stage is to turn it into a more production-oriented AI application.

1. 🗄️ Move from SQLite → MongoDB

Replace the current SQLite persistence layer with MongoDB for scalable storage of:

Users

Chat threads

Messages

Chat metadata

Conversation settings

Agent execution history

Possible structure:

users
  ↓
conversations
  ↓
messages

MongoDB would make the application easier to extend into a multi-user production system.

2. 🔐 Authentication

Add authentication using:

Supabase Auth

Google OAuth

Email/password authentication

This would allow each user to securely access only their own conversations and data.

User
 ↓
Authentication
 ↓
User ID
 ↓
User Conversations
 ↓
Messages

3. ⚛️ Replace Streamlit with React

Upgrade the frontend from Streamlit to a modern React application.

Planned stack:

React

TypeScript

Tailwind CSS

Framer Motion

React Query

Modern component-based UI

This would provide more control over:

Chat animations

Streaming responses

Thread sidebar

Message rendering

Markdown/code blocks

Loading states

Responsive layouts

Authentication screens

4. 🎨 Modern AI Chat UI

Build a production-style interface inspired by modern AI assistants.

Potential features:

Streaming responses

Message regeneration

Copy response

Markdown rendering

Code highlighting

File upload

Conversation search

Rename/delete conversations

Chat pinning

Dark/light mode

Smooth Framer Motion animations

5. 🔌 MCP Integration

Add Model Context Protocol (MCP) so the chatbot can interact with external tools and data sources.

Potential tools:

MCP
 ├── Database tools
 ├── File tools
 ├── Search tools
 ├── API tools
 ├── Business tools
 └── Internal company tools

This would move the project from a simple chatbot toward a tool-using AI assistant.

6. 🤖 Agentic Workflows

Extend the LangGraph workflow into a multi-step agent system.

Example:

User
 ↓
Router Agent
 ↓
 ├── RAG Agent
 ├── Web/Search Agent
 ├── Database Agent
 ├── MCP Tool Agent
 └── General LLM
          ↓
      Final Answer

LangGraph can be used to control these workflows and decide which tool or agent should handle a request.

7. 🔄 n8n Integration

Integrate n8n for automation and external workflows.

Example:

Chatbot
   ↓
n8n Workflow
   ↓
 ├── Send Email
 ├── Create Ticket
 ├── Update CRM
 ├── Google Sheets
 ├── Slack / Teams
 └── Database Operation

This would allow the chatbot to perform actions rather than only generate answers.

8. ⏰ Cron Jobs & Background Tasks

Add scheduled jobs for tasks such as:

Updating the knowledge base

Re-indexing documents

Cleaning old conversations

Generating analytics

Syncing external data

Updating embeddings

Scheduled reports

Example:

Cron Job
   ↓
Fetch New Documents
   ↓
Process Documents
   ↓
Generate Embeddings
   ↓
Update Vector Store

9. ☁️ Production Deployment

Move from local Streamlit execution toward a production architecture.

Planned deployment:

                ┌───────────────┐
                │    React UI   │
                │   Vercel      │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Backend API │
                │ Python / FastAPI
                └───────┬───────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
         MongoDB      Vector DB   LLM
                        │
                     RAG / MCP

Potential infrastructure:

Vercel for frontend

Python backend

MongoDB for application data

Dedicated/vector database for RAG

Hugging Face or another LLM provider

LangSmith for observability

n8n for automation

10. 📈 Advanced RAG

Improve the current basic RAG pipeline with:

Better chunking strategies

Metadata filtering

Hybrid search

Reranking

Query rewriting

Multi-query retrieval

Conversational retrieval

Citation/source display

Document-level permissions

Incremental indexing

The goal is to evolve from:

Basic RAG
PDF → Chunks → Embeddings → FAISS → LLM

to:

Production RAG
Documents
   ↓
Ingestion Pipeline
   ↓
Chunking + Metadata
   ↓
Embeddings
   ↓
Vector / Hybrid Search
   ↓
Reranker
   ↓
Relevant Context
   ↓
LLM
   ↓
Citations + Answer

🎯 Project Evolution

Version 1 — Prototype

Streamlit
   +
Mistral-7B
   +
LangChain
   +
SQLite

Version 2 — RAG Chatbot

Streamlit
   +
Mistral-7B
   +
LangGraph
   +
RAG
   +
FAISS
   +
SQLite

Version 3 — Production AI Assistant

React + Tailwind + Framer Motion
              ↓
        Authentication
              ↓
         Backend API
              ↓
       LangGraph Agents
        ↙     ↓      ↘
      RAG    MCP     n8n
        ↘     ↓      ↙
          Mistral / LLM
              ↓
           MongoDB
              ↓
        Observability

🧠 What This Project Demonstrates

This project demonstrates practical experience with:

Large Language Models

Prompt engineering

LangChain

LangGraph

Retrieval-Augmented Generation

Embeddings

Vector databases

Conversational memory

Multi-threaded chat systems

Persistent state

Agentic workflows

Tool calling

MCP

AI observability

Full-stack AI application development

The long-term goal is to evolve this from a Streamlit LLM chatbot prototype into a production-ready, full-stack AI agent platform.

📌 Status

Current: Streamlit + LangGraph + Mistral-7B + SQLite + FAISS RAG

Planned: React + Tailwind CSS + Framer Motion + MongoDB + Supabase Auth + MCP + n8n + Agentic Workflows + Cron Jobs + Production Deployment
