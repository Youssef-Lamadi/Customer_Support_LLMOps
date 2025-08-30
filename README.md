🤖 Customer Support Chatbot with LLMOps
📌 Project Overview

This project is a Customer Support Chatbot enhanced with LLMOps practices.

It was developed in two main phases:

RAG-based Chatbot – Retrieve answers from raw data sources (PDFs, FAQs, CSVs, etc.) using embedding + vector search.

LLMOps Integration – Automating the data pipeline from ingestion to deployment, with monitoring, evaluation, and tracking.

The chatbot is designed to help organizations (e.g., COD Network) provide automated, intelligent, and reliable customer support.

🚀 Features

📂 Data Ingestion: Supports multiple sources (FAQs, PDFs, CSVs).

🔎 Two-Step Retrieval: First search FAQ index → fallback to PDF index.

📚 RAG (Retrieval-Augmented Generation) for contextual answers.

🗄 Vector Database (Pinecone) storage for embeddings.

⚙️ Automated Data Pipeline: ingestion → preprocessing → indexing → storage.

📊 Experiment Tracking & Monitoring (MLflow, Weights & Biases).

🧪 Evaluation of chatbot responses with metrics.

📜 Logging for pipeline and chatbot queries.

🌐 Deployment as a web app (Flask backend + React frontend).

🏗️ System Architecture

                ┌──────────────────────┐
                │   Data Sources        │
                │  (PDFs, FAQs, CSVs)   │
                └─────────┬────────────┘
                          │
                ┌─────────▼───────────┐
                │   Data Pipeline      │
                │ (Ingestion, ETL)     │
                └─────────┬───────────┘
                          │
                ┌─────────▼──────────────┐
                │   Vector DB (Pinecone) │
                │   + Embeddings         │
                └─────────┬──────────────┘
                          │
                ┌─────────▼─────────────┐
                │   RAG Retriever        │
                │  (FAQ → PDF fallback)  │
                └─────────┬─────────────┘
                          │
                ┌─────────▼───────────┐
                │   LLM (OpenAI/GPT)  │
                │   + Monitoring/Logs │
                └─────────┬───────────┘
                          │
                ┌─────────▼──────────┐
                │   Frontend (Chat)  │
                └────────────────────┘


🛠️ Tech Stack
📂 Repository Structure
⚙️ Installation
▶️ How to run?

AWS CI&CD Deployment with Github Actions


👨‍💻 Author
    Lamadi [(https://github.com/Youssef-Lamadi)] – PFA Project (ENSA Al Hoceima)

📜 License
    This project is licensed under the MIT License – see the LICENSE file.

Chatbot Deployment on Azure

1. create azure container registry 
2. create azure virtual machine 
    connect to the VM SSH using Azure CLI
    Install Docker on the VM

    `sudo apt-get update -y && sudo apt-get upgrade -y
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    newgrp docker
    docker --version
    `

3. Github Actions fro CI&CD
    go to your repository -> settings -> Actions -> Runners
    click on New self hosted runner
    runner image select Linux + Architecture x64
    Execute the commands showen there in your Azure VM CLI

    now, set the secrets keys
    go to your repository -> settings -> Secrets and Variables -> Actions
    click on new repository secret
    add these secrets keys :
        ACR_LOGIN_SERVER = e.g. cschatbot.azurecr.io
        ACR_USERNAME = (from ACR → Access keys)
        ACR_PASSWORD = (from ACR → Access keys) 
        AZURE_CREDENTIALS = value is a json file 
        to get the json file run this command :
        az ad sp create-for-rbac --name "github-actions" --role contributor --scopes /subscriptions/<subscribtionid> --sdk-auth

        AZURE_REGION 
        ACR_REPO = Your repository name in ACR when to store the docker image
        IMAGE_NAME = the name of the docker image
        OPENAI_API_KEY
        PINECONE_API_KEY

    create .github/workflows/cicd.yaml and add the code needed to it.

4. push your code to trigger the ci cd pipeline oki



5. ## 📥 Automated Data Ingestion Pipeline

To ensure that the chatbot always has access to the most recent documents, this project includes an **automated data ingestion pipeline** powered by GitHub Actions.

### 🔄 How it works
- The workflow file [`data-ingestion.yaml`](.github/workflows/data-ingestion.yaml) is configured to **trigger automatically** whenever files inside the `data/` folder (e.g., PDF documents) are added, updated, or deleted.
- Once triggered, the workflow:
  1. Checks out the repository.
  2. Sets up the Python environment.
  3. Installs all dependencies from `requirements.txt`.
  4. Executes the script [`src/store_index.py`](src/store_index.py).

### ⚙️ What the script does
The ingestion script performs the following steps:
1. **Document parsing** → Reads all PDF files located in the `data/` directory.
2. **Text preprocessing** → Splits each document into smaller text chunks for efficient processing.
3. **Embedding generation** → Converts each chunk into vector embeddings using OpenAI’s API.
4. **Vector storage** → Uploads these embeddings into **Pinecone Vector Database**, making the content instantly searchable.

### ✅ Why this matters
- Every time you update the documents in the `data/` folder, the ingestion workflow ensures that the knowledge base is refreshed without manual intervention.
- This keeps the RAG-based chatbot always in sync with the **latest information**.

### This will show a little badge:
![Data Ingestion Pipeline](https://github.com/Youssef-Lamadi/Customer_Support_LLMOps/actions/workflows/data-ingestion.yaml/badge.svg)

    
    🟢 Green = last ingestion run succeeded
    🔴 Red = last ingestion run failed
    ⚪ Grey = no runs yet
