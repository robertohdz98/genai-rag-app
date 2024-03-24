""" Main app frontend file."""

import time

import requests
import streamlit as st

st.set_page_config(
    page_title="Your CV Chatbot!",
    page_icon=":robot_face:",
)

# Logo as header
st.image("/app/images/logo.png", use_column_width=True)

# Basic UI for users
st.title("Ask about your CV! :briefcase: :page_with_curl:")
st.header("Upload a CV and then you could ask information \
        about it directly without checking the entire resume.")

uploaded_cv = st.file_uploader(
    label="Upload your CV here. Only PDF formats are allowed.",
    type="pdf",
)

if uploaded_cv:
    with st.spinner("Reading CV. Please wait..."):
        time.sleep(5)
        # 1. OCR: read CV
        # 2. Compute embeddings
        # 3. Store embeddings in VectorDB
        # RAG

    st.write("CV uploaded successfully.")

st.text("")

user_question = st.text_area("What do you want to know?")

if len(user_question) > 0:
    ask = st.button("Get answer")

    if ask:
        question = {'question': user_question}
        r = requests.post(
            url="http://host.docker.internal:8000/question",
            json=question,
            timeout=200
        )

        st.text_area(r.content)
