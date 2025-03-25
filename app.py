from flask import Flask, request, jsonify
from src.helper import get_llm
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the LLM
llm = get_llm()

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

# Create prompt template with improved medical context
system_prompt = (
    "You are a medical knowledge assistant specialized in providing accurate and concise medical information. "
    "Use the following pieces of retrieved context to answer the medical question. "
    "If you don't know the answer or if the context doesn't provide enough information, say that you don't know. "
    "Keep your answers concise (3-4 sentences maximum) and focused on medical facts. "
    "Always maintain a professional and clear tone."
    "\n\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Create chains
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400
        
        question = data['question']
        response = rag_chain.invoke({"input": question})
        
        return jsonify({
            'answer': response['answer']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
