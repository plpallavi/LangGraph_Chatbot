import streamlit as st
from chatbotDB_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# *************************************** Utility functions **********************************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_histroy'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable' : {'thread_id' : thread_id}}).values['messages']


# ******************************************* Session Setup *********************************************
if 'message_histroy' not in st.session_state:
    st.session_state['message_histroy'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# ******************************************Sidebar UI *************************************************

st.sidebar.title('Langraph Chatbot')

if st.sidebar.button('New chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages =[]

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_histroy'] = temp_messages


# *****************************************Main UI *****************************************************
#loading the conversation histroy
for message in  st.session_state['message_histroy']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input =st.chat_input('Type here')

if user_input:
    #first add the message to message_histroy
    st.session_state['message_histroy'].append({'role' : 'user', 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)


    #st.session_state -> dict ->
    CONFIG = {'configurable' : {'thread_id' : st.session_state['thread_id']}}

    #first add the message to message_histroy
    with st.chat_message('assistant'):


        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                    {'messages' : [HumanMessage(content=user_input)]},
                    config = CONFIG,
                    stream_mode = 'messages'
            )
        )

        st.session_state['message_histroy'].append({'role' : 'assistant', 'content' : ai_message})

