from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import google.generativeai as gemini_ai

load_dotenv()

app = Flask(__name__)

# Configure Google Gemini API Key
gemini_ai.configure(api_key=os.getenv('GEMINI_API_KEY'))
REPLIERS_KEY = os.getenv('REPLIERS_KEY')


@app.route('/property_chat', methods=['GET', 'POST'])
def property_chat():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('message')

        # Make the Repliers API call
        response_from_api = get_repliers_data(user_input)

        # Integrate the response into a conversation with the Gemini model
        if response_from_api:
            prompt = f"User Query: {user_input}\n\nAPI Response: {response_from_api}"
            response = gemini_ai.chat(prompt=prompt)
            chatbot_response = response['messages'][0]['content']  # Adjust based on the actual response
        else:
            chatbot_response = "Sorry, I couldn't retrieve any data for that query."

        return jsonify({'response': chatbot_response})
    
    return "This route only accepts POST requests."


def get_repliers_data(user_query):
    """Function to query the Repliers API based on user's input"""
    API_ENDPOINT = 'https://api.repliers.io/listings'

    # Set up basic parameters for the API call (adjust as needed)
    params = {
        'cluster': 'true',
        'minPrice': '1',
        'maxPrice': '10000000',
        'numBedrooms': '1',
        'numBathrooms': '1',
        'propertyType': 'House',  # Adjust dynamically based on user input
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {REPLIERS_KEY}"  # Make sure this matches the API's expected header format
    }

    try:
        response = requests.get(API_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        data = response.json()

        # Process the API data for the chatbot to use
        if 'listings' in data and len(data['listings']) > 0:
            listings = data['listings']
            first_listing = listings[0]  # Get the first listing as an example
            return f"Listing found: {first_listing['address']}, Price: ${first_listing['listPrice']}, Bedrooms: {first_listing['details']['numBedrooms']}, Bathrooms: {first_listing['details']['numBathrooms']}"
        else:
            return None

    except requests.RequestException as e:
        print(f"Error fetching data from Repliers API: {e}")
        return None


if __name__ == '__main__':
    app.run(debug=True)
