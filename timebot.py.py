import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TimeBot", layout="centered")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash-lite"
DATA_FILE = "chat_history.json"

# ---------------- JSON HELPERS ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"interactions": []}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"interactions": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_interaction(query, response):
    data = load_data()
    data["interactions"].append({
        "query": query,
        "response": response,
        "time": datetime.now().isoformat(),
        "is_quizzed": False
    })
    save_data(data)

# ---------------- QUIZ CHECKER ----------------
def check_for_quizzes():
    if st.session_state.quiz_active:
        return

    data = load_data()
    now = datetime.now()

    for interaction in data["interactions"]:
        if interaction["is_quizzed"]:
            continue

        query_time = datetime.fromisoformat(interaction["time"])

        if now - query_time >= timedelta(minutes=10):
            generate_quiz(interaction)
            interaction["is_quizzed"] = True
            save_data(data)
            break

def generate_quiz(interaction):
    quiz_prompt = (
        "Create a short conceptual quiz question based on the following query. "
        "Do NOT give the answer.\n\n"
        f"Query: {interaction['query']}"
    )

    quiz_response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[types.Content(
            role="user",
            parts=[types.Part(text=quiz_prompt)]
        )]
    )

    st.session_state.quiz_question = quiz_response.text
    st.session_state.quiz_topic = interaction["query"]
    st.session_state.quiz_active = True

#  SESSION STATE INIT 
if "chat" not in st.session_state:
    st.session_state.chat = []

if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = None

# ---------------- CHECK FOR DUE QUIZZES ----------------
check_for_quizzes()

# ---------------- UI ----------------
st.title("🕒 TimeBot")
st.caption("Each query is quizzed exactly 10 minutes after it is asked.")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT MODE ----------------
if not st.session_state.quiz_active:
    if prompt := st.chat_input("Ask me anything"):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.chat.append({"role": "user", "content": prompt})

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )]
        )

        reply = response.text
        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.chat.append({"role": "assistant", "content": reply})
        save_interaction(prompt, reply)

# ---------------- QUIZ MODE ----------------
else:
    with st.chat_message("assistant"):
        st.markdown("### 🧠 Quiz Time!")
        st.markdown(st.session_state.quiz_question)

    if answer := st.chat_input("Answer the quiz question"):
        evaluation_prompt = (
            "Evaluate the answer.\n"
            f"Question: {st.session_state.quiz_question}\n"
            f"Answer: {answer}"
        )

        evaluation = client.models.generate_content(
            model=MODEL_NAME,
            contents=[types.Content(
                role="user",
                parts=[types.Part(text=evaluation_prompt)]
            )]
        )

        with st.chat_message("assistant"):
            st.markdown("### 📝 Evaluation")
            st.markdown(evaluation.text)

        # reset quiz state
        st.session_state.quiz_active = False
        st.session_state.quiz_question = None
        st.session_state.quiz_topic = None
