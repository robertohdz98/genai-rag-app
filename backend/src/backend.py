""" Backend API specification."""
import logging
import os
from pydantic import BaseModel

import pytesseract
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from minio import Minio, S3Error
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from pdf2image import convert_from_path


# FastAPI main configuration
app = FastAPI(
    title="My CV Chatbot API"
)


class Question(BaseModel):
    """ Quote from the user to be answered by MyCVChatbot."""
    question: str


class Context(BaseModel):
    """ Context to be used to answer the quotes from the user."""
    cv_name: str


@app.get("/")
def redirect():
    """ Redirects response to Swagger UI."""
    return RedirectResponse("/docs")


@app.post("/read_cv")
async def read_uploaded_cv(cv_filename: str):
    """ Reads a CV using Tesseract OCR."""

    # Initialize S3 client
    s3_client = Minio(
        endpoint=S3_ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False
    )

    # Download PDF file from S3
    try:
        bucket = "cvs"
        s3_client.fget_object(
            bucket_name=bucket,
            object_name=cv_filename,
            file_path=f"/tmp/{cv_filename}")
        logging.info("[%s] loaded.", cv_filename)

    except S3Error as exc:
        print(exc)
        raise HTTPException(
            status_code=404,
            detail=f"[{cv_filename}] not found in [{bucket}] bucket."
        ) from exc

    # OCR: read cv content
    cv_pages = convert_from_path(f"/tmp/{cv_filename}")

    cv_content = []
    for page in cv_pages:
        text = pytesseract.image_to_string(page)
        cv_content.append(text)

    # Store cv content as txt file
    cv_name = cv_filename.split(".")[0]
    output_cv_text = f"{cv_name}.txt"
    with open(output_cv_text, "w", encoding="utf-8") as f:
        for page in cv_content:
            f.write(page)
    print(f"[{cv_filename}] content read using OCR.")
    logging.info("[%s] content read using OCR.", cv_filename)

    return "ok"


@app.post("/ask_chatbot")
def answer_question(
    question: Question,
    context_cv: Context,
    model: str = "gpt-3.5-turbo-0125"
):
    """ Answers provided question based on context using GPT models."""

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=model)

    template = """ You are an HR consultant, skilled in extracting useful
        information from a provided curriculum. Answer the question based only
        on the provided context below. If you cannot find any information
        related so you cannot answer it, just reply 'I do not know'.

        Context: {context}
        Question: {question}
    """

    # Build our chain
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | parser

    context_cv_content = context_cv.cv_name + ".txt"
    with open(context_cv_content, "r", encoding="utf-8") as f:
        context = f.read()

    answer = chain.invoke({
        "context": context,
        "question": question.question
    })

    return answer


if __name__ == "__main__":

    # Get environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    S3_ENDPOINT = "host.docker.internal:9000"  # TODO: as env var
    ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
    SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")

    uvicorn.run(app)
