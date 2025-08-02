# from itertools import zip_longest
# from streamlit_chat import message
# import streamlit as st
# from langchain_community.chat_models import ChatOpenAI
# from langchain.schema import (
#     SystemMessage,
#     HumanMessage,
#     AIMessage,
#   )


# openapi_key="sk..xxxxxxxxxxxxxxxxxxxxxxxx"

# st.set_page_configure(page_title="legend AI")
# st.title("zain_gpt")

# if 'generated' not in st.session_state:
#     st.session_state ['generated']=[]

# if 'past' not in st.session_state:
#     st.session_state ['past']=[]

# if 'entered prompt' not in st.session_state:
#     st.session_state ['entered prompt']=[]


# Chat=ChatOpenAI(
#     temperature=0.5,
#     model_name="gpt-3.5-turbo",
#     open_api_key=openapi_key
#     )

# def get_text():
#     input_text=st.text_input("you: ",st.session_state['entered prompt'],key="input")
#     return input_text


# user_input = st.text_input("You: ")

# if user_input:
#     message=[
#         SystemMessage(content="you are a helpful AI mentor"),
#         HumanMessage(content=user_input)
#     ]

# responce=Chat(message)
# st.session_state['past'].append(user_input)
# st.session_state['generated'].append(responce.content)


# if st.session_state['generated']:
#     for user_msg, ai_msg in zip_longest(st.session_state['past'],st.session_state['generated']):
#         if user_msg:
#             message(user_msg,user=True)
#             if ai_msg:
#                 message(ai_msg)



import streamlit as st
from streamlit_chat import message
from transformers import pipeline, set_seed
from itertools import zip_longest

# Set up Streamlit page
st.set_page_config(page_title="Legend AI")
st.title("zain_gpt (Free Hugging Face Chatbot)")

# Initialize chat memory
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""

# Load the Hugging Face chatbot (free and no API key needed)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="microsoft/DialoGPT-medium")

chatbot = load_model()

# Get user input
user_input = st.text_input("You:", key="input")

# If user sends a message
if user_input:
    # Generate response using Hugging Face model
    set_seed(42)  # Optional: reproducible responses
    full_prompt = f"{user_input}"
    response = chatbot(full_prompt, max_length=1000, do_sample=True, top_p=0.95, temperature=0.7)[0]['generated_text']

    # Extract only the bot's reply (trim input from response)
    bot_reply = response[len(full_prompt):].strip()

    # Save chat
    st.session_state.past.append(user_input)
    st.session_state.generated.append(bot_reply)

# Display chat messages
if st.session_state['generated']:
    for user_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if user_msg:
            message(user_msg, is_user=True)
        if ai_msg:
            message(ai_msg)

