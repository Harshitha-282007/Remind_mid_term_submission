
import streamlit as st 
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
from datetime import datetime
import random 

# config and api key 
st.set_page_config(page_title = "Gemini clone", layout = "centered")
load_dotenv()
client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash-lite"
DATA_FILE = "chat_history_last_5.json"


# get random query from the history or retuens none if no interactions 
def get_random_query_from_history():
    interactions = st.session_state.last_five_queries
    if not interactions :
        return None 
    return random.choice(interactions)


st.title("Gemini Chatbot Clone")

# temp history for the showing of chat 
if "chat" not in st.session_state:
    st.session_state.chat = []
for msg in st.session_state.chat :
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if "query_counter" not in st.session_state :
    st.session_state.query_counter =0
if "last_five_queries" not in st.session_state:
    st.session_state.last_five_queries = []
if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = None
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if not st.session_state["quiz_active"]:
    if prompt := st.chat_input("Ask me anything"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat.append({"role":"user", "content": prompt })

        st.session_state["query_counter"] +=1
        st.session_state["last_five_queries"].append(prompt)
        if st.session_state["query_counter"] ==5:
            st.session_state["quiz_active"] = True

        response = client.models.generate_content(
            model = MODEL_NAME,
            contents = [
                types.Content(
                    role = "user",
                    parts = [types.Part(text = prompt)]
                )
            ]
        )
        reply = response.text
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.chat.append({"role":"assistant", "content": reply }) 

else :
    # --------------Quiz functionality --------------

    if st.session_state.quiz_question is None :
        quiz_source = get_random_query_from_history()

        if quiz_source is None :
            st.sidebar.markdown("No interactions to quiz from yet!!")
        
        else :
            quiz_prompt = (
                "Create a short conceptual quiz question based on the following topic. "
                "Do NOT give the answer.\n\n"
                f"Topic: {quiz_source}"
            )

            quiz_response= client.models.generate_content(
            model = MODEL_NAME,
            contents = [
                types.Content(
                    role = "user",
                    parts = [types.Part(text = quiz_prompt)]
                )
            ]
            )

            st.session_state.quiz_topic = quiz_source 
            st.session_state.quiz_question = quiz_response.text

    if st.session_state.quiz_question:
        with st.chat_message("assistant"):
            st.markdown("### 🧠 Quiz Question")
            st.markdown(st.session_state.quiz_question)
            
        if user_answer := st.chat_input("Answer the quiz question"):
            with st.chat_message("user"):
                st.markdown(user_answer)
            evaluation_prompt = (
            "You are an examiner.\n\n"
            f"Topic: {st.session_state.quiz_topic}\n\n"
            f"Question: {st.session_state.quiz_question}\n\n"
            f"Student Answer: {user_answer}\n\n"
            "Decide whether the answer is correct or incorrect. "
            "Start your response with either 'Correct:' or 'Incorrect:' "
            "and then give a brief explanation."
            )
    
            evaluation_response = client.models.generate_content(
                model = MODEL_NAME,
                contents = [
                    types.Content(
                        role = "user",
                        parts = [types.Part(text = evaluation_prompt)]
                    )
                ]
            )
            with st.chat_message("assistant"):
                st.markdown("### 📝 Evaluation")
                st.markdown(evaluation_response.text)
            st.session_state.quiz_active = False
            st.session_state.last_five_queries = []
            st.session_state.query_counter = 0 
            st.session_state.quiz_question = None
            st.session_state.quiz_topic = None









