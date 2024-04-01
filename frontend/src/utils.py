""" Utils and auxiliary functions."""

import requests


def ask_chatbot(question: str, cv_name: str, model: str, endpoint: str):
    """ Given a GPT model, asks a question regarding a specific cv_name.

    Args:
    ----
        - question: a question from the recruiter.
        - cv_name: name of the filename to look into as context.
        - model: GPT model version to be used.
        - endpoint: backend API endpoint.

    Returns:
    -------
        - response: chatbot answer to the provided question.
    """

    user_question = {"question": question}
    cv_filename = {"cv_name": cv_name}

    response = requests.post(
        url=f"http://{endpoint}/ask_chatbot",
        json={
            "question": user_question,
            "context_cv": cv_filename,
            "model": model
        },
        timeout=2000
    )

    return response.text
