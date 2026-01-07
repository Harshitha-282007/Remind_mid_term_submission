import streamlit as st
from google import genai
from dotenv import load_dotenv
import os 
from google.genai import types

# load api from env 
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

# configure gemini
client = genai.Client(api_key = API_KEY)

st.title("Gemini clone")
# set default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gemini-2.5-flash-lite"


# initiate chat history 
if "messages" not in st.session_state:
    st.session_state.messages = []

# display messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# given prompt expect response 
if prompt := st.chat_input("Ask anything"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role":"user","content":prompt})

    # single turn conversation , with part 
    # message = types.Content(
    #     role = "user",
    #     parts = [types.Part.from_text(text = prompt)]
    # )

    # multiturn conversation 
    converstaion = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        converstaion.append(
            types.Content(
                role = role,
                parts = [types.Part.from_text(text = msg["content"])]
            )
        )
    
    try : 
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = converstaion
        )
    except Exception as e:
        st.markdown(f"Error: {e}")
    else:
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role":"assistant","content":response.text})



