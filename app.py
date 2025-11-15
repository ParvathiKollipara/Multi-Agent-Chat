import streamlit as st
from agent import respond

st.title("Google AI Chatbot")

user_input = st.text_input("Ask something here...")

if st.button("Send"):
    if user_input.strip():
        answer = respond(user_input)
        st.write(answer)
    else:
        st.warning("Please type something!")
