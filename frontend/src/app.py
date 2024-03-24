""" Main app frontend file."""

import streamlit as st

st.image("/images/logo.png", use_column_width=True)

# Basic UI for users
st.title("Ask about your CV!")
st.header("Upload a CV in PDF format and then you could ask information \
    about it directly without checking the entire resume.")

uploaded_cv = st.file_uploader(
    label="Upload your CV here. Only PDF formats are allowed.",
    type="pdf",
)

if uploaded_cv:
    st.write("CV uploaded successfully.")

user_question = st.text_area("Question:")

st.button("Get answer")
