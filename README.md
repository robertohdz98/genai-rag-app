# GenAI RAG App: Your CV Chatbot! :robot:

This demo project aims to serve as a basic **POC of a RAG (Retrieval Augmented Generation) application to extract insights from provided curriculums**, enabling direct questions from a recruiter to our CV Chatbot so that reading the entire CV information would not be needed. This allows:

- Asking direct questions about a candidate's experience or background
- Gaining insights from a CV quicker
- Checking specific strenghts of a candidate
- Asking about languages, courses... (if provided)

</br>

# Table of contents
- [Monorepo structure](#monorepo-structure)
- [Modules](#modules)
- [Deployment](#deployment-using-docker-compose)
- [Tools used](#tools-used)
- [Authors](#authors)

</br>

# Monorepo structure

    ├── .devcontainer                  <--- Development environments setup
    ├── backend
    │     ├── notebooks                <--- Jupyter notebooks for tests and exploration
    │     ├── src/rag_module           <--- Source code for backend + RAG (TBD)      
    |     ├── api.Dockerfile           <--- Backend API Dockerfile
    │     ├── poetry.lock              <--- Poetry dependencies (do not edit)
    │     ├── pyproject.toml           <--- Module dependencies
    │     └── README.md                <--- Basic backend description
    │
    ├── frontend
    |     ├── images                   <--- Assets or frontend ui images
    │     ├── src/app.py               <--- Frontend initialization script
    |     ├── app.Dockerfile           <--- Frontend app Dockerfile
    │     ├── poetry.lock              <--- Poetry dependencies (do not edit)
    │     ├── pyproject.toml           <--- Module dependencies
    │     └── README.md                <--- Basic frontend description
    │
    ├── docker-compose.yaml            <--- deployment file using docker-compose
    └── README.md                      <--- Top-level description of the project

</br>

# Modules
**Your CV Chatbot! app** mainly consists on two modules:

- A **frontend app** based on Streamlit, that allows the user to upload his/her CV in PDF format to start asking questions about the candidate's profile.

![Front](https://github.com/robertohdz98/genai-rag-app/assets/68640342/b5dfb277-b3c3-43cf-b067-091eda85d77c)

- A **backend API** based on FastAPI, that reads a CV using OCR techniques and serves the OpenAI model the information provided in the CV as a context to answer questions.

Besides, a **S3 Storage** (MinIO) is used to locally store PDF files (as a bypass service due to latency issues while transferring a file via HTTP POST request).

For example, given a provided CV, the recruiter could directly ask about the most
meaningful achievement or major of the candidate to check if he or she fits the 
requirements of the vacancy:

![Question](https://github.com/robertohdz98/genai-rag-app/assets/68640342/b28c9a0c-6880-4053-921e-94721f53562f)

</br>

# Deployment (using docker-compose)

To locally deploy all the services involved in this POC in your PC, just run the following command from the root directory of the repository:

``` docker-compose --env-file .env up```

*NOTE: docker-compose is therefore a prerequisite.*

</br>

# Tools used

- **Poetry** for dependency management
- **DevContainers** for module development environments in a monorepo setup
- **LangChain** as LLM integration framework to use **OpenAI GPT models**
- **Tesseract** as OCR engine
- **FastAPI** for backend
- **Streamlit** for frontend
- **MinIO** as S3 storage server
- **Docker** to package modules as images
- **Docker Compose** to locally deploy all services together

</br>

# Authors
Roberto Hernández Ruiz (@robertohdz98)