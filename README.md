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
