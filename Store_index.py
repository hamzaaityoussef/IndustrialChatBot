from pinecone import Pinecone, ServerlessSpec
from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from dotenv import load_dotenv
import os
from langchain_core.documents import Document

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# Connect to Pinecone (new style)
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "industrial"


# Create the index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Load and process your PDF
extracted_data = load_pdf_file(data='Data/')
text_chunks = text_split(extracted_data)
embeddings_model = download_hugging_face_embeddings()

# Connect to the index
index = pc.Index(index_name)

# Prepare data to upsert
vectors = []
for i, chunk in enumerate(text_chunks):
    # Create embedding
    embedding = embeddings_model.embed_query(chunk.page_content)
    vectors.append({
        "id": f"chunk-{i}",
        "values": embedding,
        "metadata": {
            "text": chunk.page_content
        }
    })

# Upsert into Pinecone
index.upsert(vectors=vectors)

print("✅ Data indexed successfully in Pinecone!")
