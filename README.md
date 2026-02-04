# 🛡️ Secure AI Audit Assistant

> **A Secure, Graph-Based Retrieval-Augmented Generation (RAG) System with Role-Based Access Control (RBAC).**

![Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI Model](https://img.shields.io/badge/Model-Llama3-orange)

---

## 📖 What is RAG? (Retrieval-Augmented Generation)

If you are new to AI engineering, **RAG** is the technique used to give an AI model (like ChatGPT or Llama) access to **private data** that it wasn't trained on.

### The Problem
Standard AI models are "frozen" in time. They don't know about your private company files, recent emails, or specific audit policies. If you ask them about a private document, they will either say "I don't know" or make up an answer (hallucination).

### The Solution (RAG)
Instead of just asking the AI immediately, this system performs a 3-step process:
1.  **Retrieve:** When you ask a question, the system first searches your uploaded PDF/TXT files for relevant paragraphs.
2.  **Augment:** It combines your question with those found paragraphs to create a "context-rich" prompt.
3.  **Generate:** It sends this combined prompt to the AI. The AI then answers your question *using only the facts found in your documents*.

**Result:** An AI that answers accurately based on your private data, with zero hallucinations.

---

## 🚀 Key Features

This project adds a layer of **Enterprise Security** on top of standard RAG:

### 1. 🔐 Role-Based Access Control (RBAC)
Not everyone should see every document. This system filters search results based on user roles:
* **Junior Auditor:** Can only access "Public" documents.
* **Manager:** Can access "Public" and "Internal" documents.
* **Admin:** Full access to "Confidential" data.
* *Smart Denial:* If a low-level user asks about a secret file, the AI detects the file exists but refuses to reveal the content.

### 2. 🕸️ Graph Visualization
* Visualizes the security architecture.
* Shows nodes (Users) connected to permissions (Data Levels), making it easy to understand who can access what.

### 3. 📜 Immutable Audit Logs
* Security requires accountability.
* Every query, upload, and access attempt is logged to a secure CSV file with timestamps and status codes (ALLOWED/DENIED).

### 4. 🧠 Local Privacy (Ollama)
* Uses **Llama 3** running locally on your machine via [Ollama](https://ollama.com).
* **No data leaves your computer.** Perfect for sensitive audit/legal documents.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io) (Python UI)
* **Database:** [ChromaDB](https://www.trychroma.com) (Vector Database for RAG)
* **AI Engine:** [Ollama](https://ollama.com) (Running Llama 3 locally)
* **Visualization:** Graphviz (Network diagrams)
* **Language:** Python 3.10+

---

## ⚡ Installation Guide

### Prerequisites
1.  **Python 3.9+** installed.
2.  **[Ollama](https://ollama.com/download)** installed and running.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/ananya101001/rag-ai-assistant.git](https://github.com/ananya101001/rag-ai-assistant.git)
cd rag-ai-assistant
