from flask import Flask, render_template, jsonify, request
from langchain_community.vectorstores import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from groq import Groq

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Get API keys
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Set environment variables
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Initialize Pinecone
index_name = "medimind"
docsearch = Pinecone.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Create retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

def generate_text_groq(prompt, max_length=500):
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # or another available model
            max_tokens=max_length,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating text: {str(e)}")
        raise
    

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        print("Input:", msg)
        
        # Retrieve relevant documents
        docs = retriever.invoke(msg)
        
        # Format context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create the prompt with context
        prompt = f"""You are a medical knowledge assistant specialized in providing accurate and concise medical information.
Use the following pieces of retrieved context to answer the medical question.
If you don't know the answer or if the context doesn't provide enough information, say that you don't know.
Keep your answers concise (3-4 sentences maximum) and focused on medical facts.
Always maintain a professional and clear tone.

Context: {context}

Question: {msg}"""
        
        # Generate response using Groq
        answer = generate_text_groq(prompt)
        print("Response:", answer)
        return str(answer)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return str(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
