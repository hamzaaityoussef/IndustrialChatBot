# IndustrialMind - AI Industrial Assistant 🤖🏭
IndustrialMind is an AI-powered assistant that provides accurate and reliable information about industrial equipment and technology using advanced natural language processing and retrieval-augmented generation.

## Features ✨

- **AI-Powered Industrial Knowledge**:  Get instant answers to questions about industrial equipment, materials, and processes.
- **Context-Aware Responses**: Answers are based on your uploaded PDF documents (e.g., "Chapitre 01Matériel I nformatique.pdf").
- **24/7 Availability**:  Access industrial information anytime, anywhere.
## in this version i use email and password fix (email : admin@example.com , password : 1234) then in next version i will add mongodb database
-Simple Authentication: Static email and password for quick access (no database required).
- Modern Embeddings: Uses HuggingFace models and Pinecone serverless for - fast, semantic search.

<!-- - **User Profiles**: Track your chat history and preferences
- **Secure Authentication**: Protected user accounts with password hashing -->

## Tech Stack 🛠️

**Backend:**
- Python 3.9+
- Flask (Web Framework)
- Pinecone (Vector Database)
- Groq API (LLM Inference)
- HuggingFace Embeddings

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5 (UI Components)

## Installation 🚀

### Prerequisites
- Python 3.9+
- Pinecone account
- Groq API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/hamzaaityoussef/IndustrialChatBot.git
   cd MediMind

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.Install dependencies:
   ```bash
   pip install -r requirements.txt 
```


4.Set up environment variables:
Create a .env file in the root directory with:
 ```bash
FLASK_SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://localhost:27017/medimindDB
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
```
5.Run the application:
```bash
python app.py
```


   
