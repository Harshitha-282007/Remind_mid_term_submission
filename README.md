# ReMind: An Agentic AI Tutor for Memory Retention

# ReMind 🧠

*A Streamlit-based AI chatbot with memory, counters, and quiz reinforcement*

## 📌 Project Description

**ReMind** is a collection of Streamlit-based chatbots built using the **Google Gemini API**.
The project explores how conversational AI can **retain context**, **track user interactions**, and **reinforce learning** through **automatically generated quizzes**.

This repository contains multiple chatbot variants, each implementing a different memory or quiz-triggering mechanism.

---

## 🚀 Features

* Multi-turn conversational memory using Streamlit session state
* Gemini API integration for content generation and evaluation
* Query-based quiz triggering
* Time-based quiz triggering
* Mode switching between chat and quiz inputs
* Persistent session variables across app reruns

---

## 🧩 Project Structure

```text
.
├── chatbot.py        # Conversational memory chatbot
├── counterbot.py     # Quiz after every 5 queries
├── timebot.py        # Quiz triggered 10 minutes after a query
├── week2.py          # Practice / extension file
├── .env              # Gemini API key (not committed)
├── chat_history.json # Stored interactions (TimeBot)
└── README.md
```

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini API
* dotenv
* JSON (for persistent storage)
* datetime & timedelta

---

## 🤖 Bots Overview

### 1️⃣ `chatbot.py` — Conversational Memory Bot

**Purpose:**
Implements a multi-turn chatbot that remembers previous messages during a session.

**Implementation Details:**

* Stores chat history in `st.session_state.messages`
* Sends the full conversation back to Gemini for context-aware responses
* Demonstrates how session state preserves data across reruns

---

### 2️⃣ `counterbot.py` — Query Counter Quiz Bot

**Purpose:**
Triggers a quiz after every **5 user queries**.

**Key Logic:**

* `query_counter` tracks number of user prompts
* `last_five_queries` stores recent topics
* When the counter reaches 5:

  * Chat mode is disabled
  * Quiz mode is enabled using a `quiz_active` flag

**Quiz Flow:**

1. Random query selected from recent interactions
2. Gemini generates a conceptual quiz question
3. User submits an answer
4. Gemini evaluates the answer
5. State resets and chat resumes

**Notable Challenge Solved:**

* Avoided conflicting inputs by switching modes instead of using multiple `st.chat_input()` fields

---

### 3️⃣ `timebot.py` — Time-Based Quiz Bot

**Purpose:**
Each query is quizzed **exactly 10 minutes after it is asked**.

**Implementation Details:**

* Stores interactions in a JSON file with timestamps
* Checks pending interactions on each rerun
* Triggers a quiz when `now - query_time >= 10 minutes`
* Ensures each query is quizzed only once

---

### 4️⃣ `week2.py`

A self-practice file intended for extending or reimplementing learned concepts.

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Running the Project

Install dependencies:

```bash
pip install streamlit python-dotenv google-generativeai
```

Run any bot:

```bash
streamlit run chatbot.py
# or
streamlit run counterbot.py
# or
streamlit run timebot.py
```

---

## 📚 Key Concepts Demonstrated

* Streamlit session state management
* State-driven UI switching
* Prompt engineering for quizzes
* Time-based event handling
* Persistent storage using JSON
* Debugging Streamlit rerun behavior

---

## ✅ Status

✔ Mid-term submission complete
✔ Core functionality implemented
✔ Modular chatbot variants


You’ve done *proper engineering thinking* here — this is GitHub-worthy work 💙
