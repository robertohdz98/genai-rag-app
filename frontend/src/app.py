""" Main app frontend file."""

import os
import time

import requests
import streamlit as st
from minio import Minio

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

        MINIO_API_HOST = "http://host.docker.internal:9000"
        ACCESS_KEY = os.getenv('MINIO_ROOT_USER', 'minio')
        SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD', 'minio123')
        s3_client = Minio(
            "host.docker.internal:9000",
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False
        )
        with open(uploaded_cv.name, "wb") as f:
            f.write(uploaded_cv.getbuffer())
        s3_client.fput_object("cvs", uploaded_cv.name, uploaded_cv.name)
        print(f"Filename [{uploaded_cv.name}] ploaded to S3 bucket.")

        cv_s3_url = f"cvs/{uploaded_cv.name}"
        requests.post(
            url=f"http://host.docker.internal:8000/get_cv/{cv_s3_url}",
            timeout=2000
        )
        # 1. OCR: read CV
        # 2. Compute embeddings
        # 3. Store embeddings in VectorDB
        # RAG

    st.success("CV uploaded successfully.")

st.text("")

user_question = st.text_area("What do you want to know?")
ask_button = st.button("Ask CV Chatbot")

if ask_button:
    if len(user_question) > 0:
        question = {'question': user_question}
        r = requests.post(
            url="http://host.docker.internal:8000/question",
            json=question,
            timeout=200
        )

        st.write(r.content)

    else:
        st.write(":warning:  Please, make a quote")
