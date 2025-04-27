from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
# from langchain_community.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient

from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
import os
from groq import Groq
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import re
from datetime import datetime, timedelta


app = Flask(__name__, static_folder='assets')
app.secret_key = os.urandom(24)  # For session management
# app.config["MONGO_URI"] = "mongodb://localhost:27017/industryDB"  # Replace with your MongoDB URI
# mongo = PyMongo(app)
bcrypt = Bcrypt(app)


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


# Initialize Pinecone client
pc = PineconeClient(api_key=PINECONE_API_KEY)

# Get index
index = pc.Index("industrial")  # Assumes it already exists

# Load it into LangChain vector store
docsearch = PineconeVectorStore(
    index=index,
    embedding=embeddings,
    text_key="text"  # or whatever key you stored documents under
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

@app.route("/favicon.ico")
def favicon():
    return "", 200

@app.route("/")
def home():
    return render_template('home.html')



@app.route("/MediMind")
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
        prompt = f"""You are an industrial knowledge assistant specialized in providing accurate and concise information about industrial equipment and technology.
        Use the following pieces of retrieved context to answer the question.
        If the context doesn't provide enough information, use your own knowledge to provide a helpful and accurate answer.
        Keep your answers concise (3-4 sentences maximum) and focused on technical facts.
        Always maintain a professional and clear tone.
        

Context: {context}

Question: {msg}"""
        
        # Generate response using Groq
        answer = generate_text_groq(prompt)
        print("Response:", answer)
         # Log the chat message to the user's history
        if 'user_id' in session:
            chat_message = {
                'user_id': session['user_id'],
                'query': msg,
                'response': answer,
                'timestamp': datetime.now()
            }
            # mongo.db.chat_history.insert_one(chat_message)
            
        return str(answer)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return str(f"An error occurred: {str(e)}")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        existing_user = mongo.db.users.find_one({'email': email})
        
        if existing_user:
            flash('Email already exists. Please use a different email or sign in.', 'danger')
            return redirect(url_for('signup'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user
        new_user = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now(),
            'membership': 'Free'
        }
        
        # Insert the user into the database
        result = mongo.db.users.insert_one(new_user)
        
        # Log the user in
        session['user_id'] = str(result.inserted_id)
        session['username'] = username
        session['email'] = email
        
        flash('Account created successfully! Welcome to MediMind.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('signup.html')



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Static credentials
        STATIC_EMAIL = "admin@example.com"
        STATIC_PASSWORD = "1234"
        
        if email == STATIC_EMAIL and password == STATIC_PASSWORD:
            session['user_id'] = "static_user"
            session['username'] = "admin"
            session['email'] = STATIC_EMAIL
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('signin'))
    
    return render_template('signin.html')            
    

# User logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Profile route
# @app.route('/profile')
# def profile():
#     if 'user_id' not in session:
#         flash('Please login to access this page', 'warning')
#         return redirect(url_for('signin'))
    
#     # Get user data
#     user = mongo.db.users.find_one({'email': session['email']})
    
#     # Get chat history for this user
#     chat_history = list(mongo.db.chat_history.find(
#         {'user_id': session['user_id']},
#         sort=[('timestamp', -1)],
#         limit=5
#     ))
#     # Get total number of chats
#     chat_count = mongo.db.chat_history.count_documents({'user_id': session['user_id']})
    
#     # Add chat count to user data for display
#     user['chat_count'] = chat_count
    
#     return render_template('profile.html', user=user, chat_history=chat_history)



# Route middleware to check if user is logged in
def login_required(route_function):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('signin'))
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__
    return wrapper

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)