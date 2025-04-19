from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC   # <-- Use this for creating index
from pinecone import ServerlessSpec
from langchain.vectorstores import Pinecone as LangchainPinecone  # <-- Avoid name conflict
from dotenv import load_dotenv
import os


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data=load_pdf_file(data='Data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


# Initialize Pinecone GRPC client
pc = PineconeGRPC(api_key=PINECONE_API_KEY)

# Create index if it doesn't exist
index_name = "medimind"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Embed documents and upsert into Pinecone index using Langchain
docsearch = LangchainPinecone.from_documents(  # ✅ use alias
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)
