from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# Configure Google Gemini API Key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
REPLIERS_KEY = os.getenv('REPLIERS_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']

    # Initialize Gemini AI
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)
    
    # Example of handling user requirements
    if 'bedroom' in user_input.lower() and 'house' in user_input.lower():
        listings = get_real_estate_listings(user_input)
        response_text = f"Here are some listings that match your criteria: {listings}"
    else:
        response_text = response.text
    
    return jsonify({'response': response_text})

def get_real_estate_listings(user_input):
    # Parse user_input to get parameters for Repliers API
    # This is a simplified example; actual implementation will need more complex parsing
    params = {
        'numBedrooms': extract_number(user_input),
        'propertyType': 'rental'
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "REPLIERS-API-KEY": REPLIERS_KEY
    }

    api_url = f'https://api.repliers.io/listings'
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        listings = response.json()
        # Process listings data as needed
        return listings
    except requests.RequestException as e:
        return f'Error fetching listings: {str(e)}'

def extract_number(text):
    match = re.search(r'\d+', text)
    return match.group() if match else None

if __name__ == '__main__':
    app.run(debug=True)
