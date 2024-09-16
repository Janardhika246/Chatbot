from flask import Flask, request, jsonify
import requests
import os
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import google.generativeai as gemini_ai

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure API keys
gemini_ai.configure(api_key=os.getenv('GEMINI_API_KEY'))
REPLIERS_KEY = os.getenv('REPLIERS_KEY')

@app.route('/property_chat', methods=['POST'])
def property_chat():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('message')

        # Get data from Repliers API based on user query
        repliers_response = get_repliers_data(user_input)

        # Generate a chat response using the Gemini model, including Repliers API data
        if repliers_response:
            prompt = f"User Query: {user_input}\n\nReal Estate Info: {repliers_response}"
            response = genai.chat(prompt=prompt)
            chatbot_response = response['messages'][0]['content']  # Adjust based on actual response
        else:
            chatbot_response = "Sorry, I couldn't retrieve any real estate data for that query."

        return jsonify({'response': chatbot_response})

    return "This route only accepts POST requests."


def get_repliers_data(user_query):
    """Queries Repliers API based on the user input"""
    API_ENDPOINT = 'https://api.repliers.io/listings'

    # Extract search filters from user query (you can improve parsing to make it more dynamic)
    params = {
        'maxPrice': '1000000',  # Example default, modify dynamically based on user query
        'city': 'New York',  # Adjust based on user input parsing
        'minBeds': '3',  # Example minimum bedrooms, adjust as per user query
    }

    headers = {
        "Authorization": f"Bearer {REPLIERS_KEY}",
        "accept": "application/json"
    }

    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        data = response.json()

        # Process the data and extract useful details
        if 'listings' in data and len(data['listings']) > 0:
            first_listing = data['listings'][0]
            return f"Listing: {first_listing['address']}, Price: ${first_listing['listPrice']}, Bedrooms: {first_listing['beds']}, Bathrooms: {first_listing['baths']}"
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching data from Repliers API: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
