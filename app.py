import streamlit as st
from agent import Agent  # This imports your Agent class from agent.py

# Create two agents
agent1 = Agent("Agent 1")
agent2 = Agent("Agent 2")

st.title("🤖 Multi-Agent Conversation Demo")

sender = st.radio("Who is sending the message?", ["Agent 1", "Agent 2"])
message = st.text_input("Enter your message:")

if st.button("Send"):
    if sender == "Agent 1":
        reply = agent2.respond(message, sender)
    else:
        reply = agent1.respond(message, sender)

    st.success(reply)
