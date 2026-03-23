# Steps to Set up the Bot

1. set-up ollama 
2. ollama pull mistral
3. python  -m venv myenv
4. activate the env
5. pip install -r requirements.txt
6. python DataLayer/testData.py -- test DataLayer
7. python LLMLayer/testLLM.py  -- test LLMLayer
8. setx TELEGRAM_BOT_TOKEN "your_actual_token_here"  --(Get this from @botFather on telegram)
9. run main.py
10. Go the telegram bot and ask querry.

# Telegram bot instructions

| Command                 | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| /ask <query>           | Runs the RAG query; shows a warning if no query is provided                |
| /help                  | Displays formatted usage instructions                                      |
| /start                 | Resumes the bot for that chat (sets polling active)                        |
| /quit                  | Pauses the bot for that chat (ignores /ask and free-text)                  |

## 🚀 What Makes This System Stand Out

### 🧩 Modular Architecture
Each component (Telegram Layer, RAG Core, Retriever, LLM, Storage) is **loosely coupled** and can be independently replaced or upgraded without affecting the rest of the system.

---

### 🧪 Highly Testable
Dedicated unit and integration tests for every layer make the system:
- Easy to debug  
- Reliable in production  
- Safe to extend and refactor  

---

### 🔄 One-Click Knowledge Switching
The system is designed to **swap knowledge bases effortlessly**:
- Load a different dataset  
- Rebuild embeddings via `DataManager`  
- Instantly reuse the same bot with new context  

**Use the same bot for multiple domains without code changes.**

---

### 🖥️ Fully Local & Private
Runs completely on local infrastructure using Ollama:
- No external API dependency  
- Better data privacy  
- Lower operational cost  

---

### ⚡ Production-Ready Design
Built with real-world considerations:
- Async Telegram handling  
- Logging and observability  
- Scalable architecture  


### This makes the system not just a demo, but a **flexible, production-ready RAG framework**.

---

#  RAG-Based Telegram Bot – System Design

##  Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system integrated with a **Telegram Bot**.

It allows users to:
- Ask questions via Telegram
- Retrieve relevant knowledge from custom data
- Generate intelligent responses using an LLM

---
##  High-Level Architecture
User (Telegram) → Telegram Bot → RAGBot → Retriever → LLM → Response
↓
StorageBackend
↑
DataManager

---
---
## Class Diagram
![Class Diagram](assets/ClassDiagram.png)
---
## Query Flow (Runtime)

1. User sends a message or `/ask` command on Telegram
2. Telegram handler receives the message
3. Query is passed to `RAGBot`
4. Query → embedding using `SentenceTransformerModel`
5. Retriever fetches top-k relevant chunks
6. Prompt is constructed using context + query
7. LLM generates response
8. Response is sent back to user
9. Interaction is logged

---
---
## Query Flow Diagram
![Query Flow](./assets/QueryFlowdaigram.png)
---
##  Components

### 1. Telegram Layer (Interface Layer)

Handles user interaction via Telegram.

#### Features:
- `/ask <query>` → Query the knowledge base
- `/start` → Activate bot
- `/quit` → Pause bot
- `/help` → Usage instructions
- Free-text support (auto-query)

#### Responsibilities:
- Manage chat state (active/paused)
- Route user input to RAG system
- Send responses back to users

---

### 2. RAGBot (Core Orchestrator)

Handles:
- Query embedding
- Retrieval
- Prompt construction
- LLM response generation
- Logging

---

### 3. DataManager (Data Pipeline)

Responsible for:
- Loading files
- Chunking text
- Generating embeddings
- Syncing with storage using hashing

---

### 4. StorageBackend (Persistence Layer)

Stores:
- Text chunks
- Embeddings
- Metadata

#### Current:
- `PickleBackend`

---

### 5. Retriever (Search Layer)

Finds relevant chunks using similarity search.

#### Current:
- `BruteForceRetriever`

---

### 6. Embedding Model

Converts text → vector

#### Current:
- `SentenceTransformerModel`

---

### 7. LLM Layer

Generates final response

#### Current:
- `OllamaLLM` (local inference)

---

### 8. PromptLogger (Observability)

Logs:
- Queries
- Context
- Responses
- Metadata

---

##  Why This Design is Useful

### ✔ Modular
Each layer is independent:
- Telegram UI can be replaced with Web UI / API
- LLM can be swapped easily
- Retriever can be upgraded

---

### ✔ Scalable
You can scale each layer independently:
- Move storage to cloud
- Replace retriever with vector DB
- Use hosted LLM APIs

---

### ✔ Extensible
Easy to add:
- Multi-user sessions
- Chat history
- Personalization

---

### ✔ Real-world Ready
- Async Telegram handlers
- Logging
- Stateful chat control (pause/resume)

---

# 💡 Use Cases 
- E-commerce assistant
- Customer support bot
- Knowledge base Q&A
- Internal company assistant

# 🧪 Testing & Validation

This project ensures reliability through **unit tests** and **end-to-end integration tests** across all layers.

---

## 🔹 Test Scripts

### 1. **Data Layer**
- **Script:** `DataLayer/testData.py`
- **Coverage:** Data loading, chunking, embedding generation, storage synchronization
- **Run:**
  ```bash
  python DataLayer/testData.py
  ```

### 2. **LLM Layer**
- **Script:** `LLMLayer/testLLM.py`
- **Coverage:** LLM setup, prompt handling, response generation
- **Run:**
  ```bash
  python LLMLayer/testLLM.py
  ```

### 3. **Integration Testing**
- **Script:** `testknowledgeRetrival.py`
- **Coverage:** Full RAG pipeline (query → retrieval → LLM → response)
- **Run:**
  ```bash
  python testknowledgeRetrival.py
  ```

---

## 🔄 **Knowledge Update Validation**
The **`DataManager`** ensures:
- Detection of changes in the knowledge base
- Reprocessing of **only updated data**
- Consistent embeddings **without full recomputation**

**Benefit:** Faster updates and resource efficiency.

---

## 💡 **Summary**
- **Reliability:** Validates correctness at every layer
- **Debugging:** Enables modular issue isolation
- **End-to-End:** Confirms system behavior as a whole