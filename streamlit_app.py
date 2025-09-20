import streamlit as st
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def load_icon():
    img = Image.open("INTQ_pfp.png")
    return img

st.set_page_config(
    page_title="INTQ AI Chat Page",
    page_icon=load_icon(),  
    layout="centered",  
    initial_sidebar_state="auto"
)

st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: #f0f0f0;
    }
    .css-1d391kg {
        color: #1c1c1c;
    }
    </style>
    """, 
    unsafe_allow_html=True
)



genai.configure(api_key="AIzaSyDY82-5HEFDBdY3P8xXLs72-7VSD6Rp-hM")
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2000,
  "response_mime_type": "text/plain",
}

if "message_history" not in st.session_state:

    st.session_state.message_history = [
            {"role": "user", "parts": ""},
    ]

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)





# params = st.query_params

# info_type = params.get("type", "")
# info_text = params.get("text", "")

# if info_text:
#     st.session_state.message_history.append(
#         {"role": "assistant", "parts": f"Context from YouTube ({info_type}): {info_text}"}
#     )
#     st.session_state.messages.append(
#         {"role": "assistant", "parts": f"Context from YouTube ({info_type}): {info_text}"}
#     )


chat_session = model.start_chat(
    history=st.session_state.message_history
)




#


def right_aligned_message(message):
    st.markdown(
        f'<div style="text-color:#000000;text-align: right; padding:10px; border-radius:16px;">{message}</div>',
        unsafe_allow_html=True
    )
def left_aligned_message(message):
    st.markdown(
        f'<div style="text-color:#000000;text-align: left; padding:10px; border-radius:16px;>{message}</div>'
    )
st.title("INTQ AI")

if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    if message['role'] == 'user':
        right_aligned_message(message['parts'])
    else:
        st.chat_message(message['role'],avatar=load_icon()).markdown(message['parts'])

prompt = st.chat_input("Chat with INTQ")
if prompt:
    right_aligned_message(prompt)
    st.session_state.messages.append({'role': 'user', 'parts': prompt})
    st.session_state.message_history.append({"role": "user", "parts": prompt})
    response = chat_session.send_message(prompt)


    st.chat_message('assistant',avatar=load_icon()).markdown(response.text)
    st.session_state.message_history.append({"role": "assistant", "parts": response.text})
    st.session_state.messages.append({"role": "assistant", "parts": response.text})
