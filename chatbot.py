import streamlit as st
import requests
from gtts import gTTS
import os

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chatbot")

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def speak_text(text):
    tts = gTTS(text, lang="en")  # Set language to English
    audio_file = "response.mp3"
    tts.save(audio_file)
    return audio_file

API_URL = "YOUR_NGROK_URL"  

with st.form("message_form"):
    user_input = st.text_input("Enter your message :")
    submitted = st.form_submit_button("Send")


if submitted and user_input:
    add_message("Utilisateur", user_input)  
    
    try:
        response = requests.post(API_URL, json={"question": user_input})
        response_data = response.json()  
        chatbot_response = response_data.get("answer", "Désolé, une erreur s'est produite.")
    except Exception as e:
        chatbot_response = "Désolé, une erreur s'est produite lors de la communication avec le serveur."

    add_message("Chatbot", chatbot_response) 

for i, message in enumerate(st.session_state.messages):
    if message["role"] == "Utilisateur":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
                <div style="margin-right: 10px;">
                    <span style="font-weight: bold;">Vous :</span> {message['content']}
                </div>
                <img src="https://cdn-icons-png.flaticon.com/512/4825/4825076.png" alt="user" width="30" height="30" style="border-radius: 50%;"/>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; align-items: center; margin-bottom: 10px;">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" alt="bot" width="30" height="30" style="border-radius: 50%; margin-right: 10px;"/>
                <div>
                    <span style="font-weight: bold;">Chatbot :</span> {message['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if st.session_state.messages and st.session_state.messages[-1]["role"] == "Chatbot":
    last_response = st.session_state.messages[-1]["content"]
    audio_file_path = speak_text(last_response)
    st.audio(audio_file_path, format="audio/mp3")
