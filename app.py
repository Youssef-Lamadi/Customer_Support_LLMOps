from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt_library.prompt import *
import os


# Create the Flask App instance
app = Flask(__name__)

# Load the Envirenment Variables from .env file
load_dotenv()

# Reads API keys from environment variables.
PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')

# set keys in runtime so Pinecone/OpenAI SDKs can access them.
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Download the embeddings model from the Hugging Face Hub.
embeddings = download_hugging_face_embeddings()

index_name = "cs-chatbot-pdfs-index" 

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Defines a retriever that finds top-3 relevant chunks (k=3) for each user query.
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# Loads GPT-4o-mini as a chat model.
chatModel = ChatOpenAI(model="gpt-4o-mini")

# Define the system prompt for the chatbot.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),          # system = rules/context from src.prompt_library.prompt
        ("human", "{input}"),               # human = placeholder for user input.
    ]
)

# Builds the RAG pipeline
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)         # puts documents + user input into the prompt.
rag_chain = create_retrieval_chain(retriever, question_answer_chain)            # retrieves docs and passes them to question_answer_chain

# Define the main route (homepage)
@app.route("/")
def chat():
    return render_template('index.html')


@app.route("/get", methods=["GET", "POST"])
def index():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)