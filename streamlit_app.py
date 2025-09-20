import streamlit as st
import google.generativeai as genai


st.set_page_config(
    page_title="TMT AI Chat Page",
    layout="centered",
    initial_sidebar_state="auto"
)

st.markdown(
    """
    <style>
    .css-18e3th9 { background-color: #f0f0f0; }
    .css-1d391kg { color: #1c1c1c; }
    </style>
    """,
    unsafe_allow_html=True
)

api_key = st.secrets["API"]
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}

if "message_history" not in st.session_state:
    st.session_state.message_history = []

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_session = model.start_chat(history=st.session_state.message_history)

def right_aligned_message(msg):
    st.markdown(f'<div style="color:#000;text-align:right;padding:10px;border-radius:16px;">{msg}</div>', unsafe_allow_html=True)

def left_aligned_message(msg):
    st.markdown(f'<div style="color:#000;text-align:left;padding:10px;border-radius:16px;">{msg}</div>', unsafe_allow_html=True)

query_params = st.query_params
fact = query_params.get("fact", [""])[0]
neutral = query_params.get("neutral", [""])[0]
more = query_params.get("more", [""])[0]
user_query = query_params.get("query", [""])[0]

if "context_data" not in st.session_state:
    st.session_state.context_data = {"fact": fact, "neutral": neutral, "more": more}


st.title("TMT AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        right_aligned_message(msg["parts"])
    else:
        st.chat_message(msg["role"]).markdown(msg["parts"])

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

prompt = st.chat_input("Chat with TMT")
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
