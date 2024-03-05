import streamlit as st

from langchain.callbacks import StreamlitCallbackHandler
from MofinChatBot.OpenAIServices import OpenAIServices
import time
chatservice = OpenAIServices()

st.image('Data/Mofinchat.png')
st.divider()

def chat(user_input, container):
    with container:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner('CHAT-BOT is at Work ...'):
                # chat agent 실행
                assistant_response = chatservice.run_agent(user_input)
                ## 만약 내부 동작 보고 싶다면 
                # st_callback = StreamlitCallbackHandler(st.container())
                # response = chatservice.run_agent(user_input, callbacks=[st_callback])

            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.splitlines():
                full_response += chunk + "\n "
                time.sleep(0.1)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
container = st.container()
with container:
    
    # Display chat messages from history on app rerun
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # button 누르기
    st.button('애플의 주가가 15년전에 비해 얼마나 올랐어?',
            type="secondary",
            on_click=chat, args=('애플의 주가가 15년전에 비해 얼마나 올랐어?', container,))
    st.button('애플 살까 테슬라 살까',
            type="secondary",
            on_click=chat, args=('애플 살까 테슬라 살까',container,))
    st.button('테슬라는 뭐하는 회사야?',
            type="secondary",
            on_click=chat, args=('테슬라는 뭐하는 회사야?',container,))
  
    if user_input := st.chat_input("What is your question?"):
        chat(user_input, container)