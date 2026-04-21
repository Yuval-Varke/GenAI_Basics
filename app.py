import streamlit as st


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("User"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "User", "content": user_input})