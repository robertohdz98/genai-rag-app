""" Main app frontend file."""

import os

import requests
import streamlit as st
from minio import Minio

# Get environment variables
API_ENDPOINT = "host.docker.internal:8000"  # TODO: as env var
S3_ENDPOINT = "host.docker.internal:9000"  # TODO: as env var
ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")

# App configuration in explorer tab
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

# CV PDF uploader
uploaded_cv = st.file_uploader(
    label="Upload your CV here. Only PDF formats are allowed.",
    type="pdf",
)

if uploaded_cv:

    @st.cache_data  # FIXME: cache cv upload when user asks
    def upload_cv():
        uploaded_file = uploaded_cv
        return uploaded_file

    with st.spinner("Uploading CV..."):
        with open(uploaded_cv.name, "wb") as f:
            f.write(uploaded_cv.getbuffer())
        # Upload CV in S3 storage bucket
        s3_client = Minio(
            endpoint=S3_ENDPOINT,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False
        )
        s3_client.fput_object("cvs", uploaded_cv.name, uploaded_cv.name)
    st.success("CV uploaded successfully.")

    with st.spinner("Reading CV. Please wait..."):
        # In the background, initialize OCR process and cv reading
        cv_filename = uploaded_cv.name.split(".")[0]
        response = requests.post(
            url=f"http://{API_ENDPOINT}/read_cv?cv_filename={uploaded_cv.name}",
            timeout=2000
        )
    st.success("CV read successfully.")

st.text("")

model = st.selectbox("GPT model",
                     ("gpt-3.5-turbo-0125", "gpt-3.5-turbo"))

st.text("")

user_question = st.text_area("What do you want to know?")
ask_button = st.button("Ask CV Chatbot")

if ask_button:
    uploaded_cv = upload_cv() # FIXME: cache cv upload when user asks
    if len(user_question) > 0:
        question = {"question": user_question}
        cv_name = {"cv_name": cv_filename}

        response = requests.post(
            url=f"http://{API_ENDPOINT}/ask_chatbot",
            json={"question": question,
                  "context_cv": cv_name,
                  "model": model},
            timeout=200
        )

        st.text_area("Response", response.text)

    else:
        st.write(":warning:  Please, make a quote")
