# Frontend: Your CV Chatbot!

This module stands for the **frontend app based on Streamlit** of our POC CV
Chatbot. The actual workflow is:

- User uploads a CV in PDF format
- To communicate smoothly with the backend API, CV is uploaded to a S3 storage
bucket (sending file through HTTP request could be too heavy and slow)
- When CV is stored in S3, a POST request is sent to the backend API to start
reading process to enable asking questions about the candidate's experience or background
- When read, user can ask sustained questions to the chatbot to gain insights or
quickly find out specific quotes
