# MediMind - AI Medical Assistant 🤖💊

![MediMind Logo](assets/img/logo.png) <!-- Add your logo if available -->

MediMind is an AI-powered medical assistant that provides accurate and reliable medical information using advanced natural language processing and retrieval-augmented generation.

## Features ✨

- **AI-Powered Medical Knowledge**: Get instant answers to medical questions
- **Context-Aware Responses**: Tailored information based on your queries
- **24/7 Availability**: Access medical information anytime, anywhere
- **User Profiles**: Track your chat history and preferences
- **Secure Authentication**: Protected user accounts with password hashing

## Tech Stack 🛠️

**Backend:**
- Python 3.9+
- Flask (Web Framework)
- MongoDB (Database)
- Pinecone (Vector Database)
- Groq API (LLM Inference)
- HuggingFace Embeddings

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5 (UI Components)

## Installation 🚀

### Prerequisites
- Python 3.9+
- MongoDB
- Pinecone account
- Groq API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MediMind.git
   cd MediMind

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.Install dependencies:
   ```bash
pip install -r requirements.txt

4.Set up environment variables:
Create a .env file in the root directory with:
 ```bash
FLASK_SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://localhost:27017/medimindDB
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key

5.Run the application:
```bash
python app.py



   
