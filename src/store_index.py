from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec 
from langchain_pinecone import PineconeVectorStore

def store_data_in_index():
    load_dotenv()

    # Access the API keys
    PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')

    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

    # Get project root (parent of "src")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data")

    embeddings = download_hugging_face_embeddings()

    pinecone_api_key = PINECONE_API_KEY
    pinecone_client = Pinecone(api_key=pinecone_api_key)

    # ======================== Working with PDF files ======================================= #
    # Read data from pdf files
    extracted_data=load_pdf_file(data=data_path)
    filter_data = filter_to_minimal_docs(extracted_data)
    text_chunks=text_split(filter_data)

    # Init Pinecone
    index_name = "cs-chatbot-pdfs-index"  
    if not pinecone_client.has_index(index_name):
        pinecone_client.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index = pinecone_client.Index(index_name)

    # Clear the index before inserting any new data
    index.delete(delete_all=True)
    
    ids = [str(i + 1) for i in range(len(text_chunks))]
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunks,
        index_name=index_name,
        embedding=embeddings, 
        ids=ids
    )

    
store_data_in_index()
