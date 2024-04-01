""" Main app frontend file."""

import os

import requests
import streamlit as st
from minio import Minio

from src.utils import ask_chatbot

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


@st.cache_data(show_spinner=False)
def read_cv(cv):
    """ Caches operation of reading and processing uploaded CV."""
    cv_name = cv.name.split(".")[0]
    response = requests.post(
        url=f"http://{API_ENDPOINT}/read_cv?cv_filename={cv.name}",
        timeout=2000
    )

    return response.status_code, cv_name


# CV PDF uploader
uploaded_cv = st.file_uploader(
    label="Upload your CV here. Only PDF formats are allowed.",
    type="pdf",
)

if uploaded_cv:

    # Store uploaded CV file in S3 storage
    with st.spinner("Uploading CV..."):
        with open(uploaded_cv.name, "wb") as f:
            f.write(uploaded_cv.getbuffer())

        s3_client = Minio(
            endpoint=S3_ENDPOINT,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False
        )
        s3_client.fput_object("cvs", uploaded_cv.name, uploaded_cv.name)
        st.success("CV uploaded successfully.")

    # In the background, initialize OCR process and CV processing
    with st.spinner("Reading CV. Please wait..."):
        status_code, cv_filename = read_cv(uploaded_cv)
        if status_code == 200:
            st.success("CV read successfully.")
        else:
            st.error("CV could not be read. Please try uploading it again")

    st.text("")

    # GPT model selector
    model = st.selectbox("GPT model", ("gpt-3.5-turbo-0125", "gpt-3.5-turbo"))

    st.text("")

    # User interaction area: make a question
    user_question = st.text_area("What do you want to know?")
    ask_button = st.button("Ask Your CV Chatbot!")

    if ask_button:
        _, cv_filename = read_cv(uploaded_cv)

        if len(user_question) > 0:
            answer = ask_chatbot(
                question=user_question,
                cv_name=cv_filename,
                model=model,
                endpoint=API_ENDPOINT
            )

            st.text_area("Response", answer)

        else:
            st.write(":warning:  Please, make a question")
