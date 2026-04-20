import streamlit as st

messages = [
    {
        "role":"User",
        "content":"Hello"
    },
    {
        "role":"AI Assistant",
        "content":"Hello! How can I assist you today?"
    }
]


for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.chat_input("Type your message here...")