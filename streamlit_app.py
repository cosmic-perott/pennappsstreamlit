import streamlit as st
from PIL import Image
import google.generativeai as genai

# -------------------------------
#  ICON LOADER
# -------------------------------

st.set_page_config(
    page_title="INTQ AI Chat Page",
    layout="centered",
    initial_sidebar_state="auto"
)

# -------------------------------
#  CUSTOM STYLING
# -------------------------------
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

# -------------------------------
#  GEMINI CONFIG
# -------------------------------
api = st.secrets.api
genai.configure(api_key=api)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2000,
  "response_mime_type": "text/plain",
}

if "message_history" not in st.session_state:
    st.session_state.message_history = [{"role": "user", "parts": ""}]

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=st.session_state.message_history
)

# -------------------------------
#  HELPER FUNCTIONS
# -------------------------------
def right_aligned_message(message: str):
    st.markdown(
        f'<div style="color:#000000; text-align: right; padding:10px; border-radius:16px;">{message}</div>',
        unsafe_allow_html=True
    )

def left_aligned_message(message: str):
    st.markdown(
        f'<div style="color:#000000; text-align: left; padding:10px; border-radius:16px;">{message}</div>',
        unsafe_allow_html=True
    )

# -------------------------------
#  READ CONTEXT FROM URL
# -------------------------------
query_params = st.experimental_get_query_params()

fact = query_params.get("fact", [""])[0]
neutral = query_params.get("neutral", [""])[0]
more = query_params.get("more", [""])[0]
user_query = query_params.get("query", [""])[0]

if "context_data" not in st.session_state:
    st.session_state.context_data = {"fact": fact, "neutral": neutral, "more": more}

# -------------------------------
#  DISPLAY TITLE + CHAT HISTORY
# -------------------------------
st.title("INTQ AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for message in st.session_state.messages:
    if message["role"] == "user":
        right_aligned_message(message["parts"])
    else:
        st.chat_message(message["role"]).markdown(message["parts"])

# -------------------------------
#  IF USER QUERY PASSED VIA URL
# -------------------------------
if user_query and not st.session_state.get("query_loaded"):
    st.session_state.messages.append({"role": "user", "parts": user_query})
    st.session_state.message_history.append({"role": "user", "parts": user_query})

    context_text = f"""
FACT CHECK: {fact}
NEUTRAL OVERVIEW: {neutral}
MORE INFO: {more}
"""

    response = chat_session.send_message(context_text + "\n\nUser: " + user_query)

    st.chat_message("assistant").markdown(response.text)
    st.session_state.message_history.append({"role": "assistant", "parts": response.text})
    st.session_state.messages.append({"role": "assistant", "parts": response.text})
    st.session_state.query_loaded = True

# -------------------------------
#  NORMAL CHAT INPUT
# -------------------------------
prompt = st.chat_input("Chat with INTQ")
if prompt:
    right_aligned_message(prompt)
    st.session_state.messages.append({"role": "user", "parts": prompt})
    st.session_state.message_history.append({"role": "user", "parts": prompt})

    # Prepend context every time
    context_text = f"""
FACT CHECK: {st.session_state.context_data['fact']}
NEUTRAL OVERVIEW: {st.session_state.context_data['neutral']}
MORE INFO: {st.session_state.context_data['more']}
"""

    response = chat_session.send_message(context_text + "\n\nUser: " + prompt)

    st.chat_message("assistant").markdown(response.text)
    st.session_state.message_history.append({"role": "assistant", "parts": response.text})
    st.session_state.messages.append({"role": "assistant", "parts": response.text})
