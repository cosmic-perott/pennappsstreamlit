import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


api = st.secrets.API
st.set_page_config(
    page_title="TMT AI Chat Page",
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



genai.configure(api_key=api)
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
st.title("TMT AI")

if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    if message['role'] == 'user':
        right_aligned_message(message['parts'])
    else:
        st.chat_message(message['role']).markdown(message['parts'])

prompt = st.chat_input("Chat with TMT")
if prompt:
    right_aligned_message(prompt)
    st.session_state.messages.append({'role': 'user', 'parts': prompt})
    st.session_state.message_history.append({"role": "user", "parts": prompt})
    response = chat_session.send_message(prompt)


    st.chat_message('assistant').markdown(response.text)
    st.session_state.message_history.append({"role": "assistant", "parts": response.text})
    st.session_state.messages.append({"role": "assistant", "parts": response.text})
