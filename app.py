import streamlit as st
from agent import Agent

agent1 = Agent("Agent 1")
agent2 = Agent("Agent 2")

st.title("🤖 Google Gemini Multi-Agent Demo")

sender = st.radio("Who is speaking?", ["Agent 1", "Agent 2"])
message = st.text_input("Enter your message:")

if st.button("Send"):
    if sender == "Agent 1":
        reply = agent2.respond(message, sender)
    else:
        reply = agent1.respond(message, sender)

    st.success(reply)
