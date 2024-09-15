from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()  # Load environment variables from a .env file

# Configure Google Gemini API Key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')

    # Integrating with Gemini AI (Google Generative AI)
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)

    # Send the chatbot's response back to the frontend
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
