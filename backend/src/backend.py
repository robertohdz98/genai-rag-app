""" Backend API specification."""
import os

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from minio import Minio
from openai import OpenAI

app = FastAPI()


@app.get("/")
def redirect():
    """ Redirects response to Swagger UI."""
    return RedirectResponse("/docs")


@app.post("/get_cv/{cv_s3_url}")
async def get_uploaded_cv(cv_s3_url: str):
    """ Reads a CV."""

    ACCESS_KEY = os.getenv('MINIO_ROOT_USER', 'minio')
    SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD', 'minio123')
    s3_client = Minio(
        "host.docker.internal:9000",
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False
    )

    bucket, filename = cv_s3_url.split("/")
    cv = s3_client.get_object(bucket, filename)

    return cv.read()


@app.post("/question")
def answer_question(question: dict):
    """ Answers provided question using GPT 3.5"""

    # vectorize question

    # ask chatgpt with context
    context = "You are a HR consultant, skilled in extracting useful \
        information from a provided curriculum."

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": context},
            {"role": "user",
             "content": question["question"]}
        ]
    )

    # return back question
    answer = response.choices[0].message.content

    print("question:", question["question"])
    print("answer:", answer)

    return answer


if __name__ == "__main__":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    uvicorn.run(app)
