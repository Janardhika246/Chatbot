from flask import Flask, render_template, request, jsonify
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load REPLIERS API key from environment variable
API_KEY = os.getenv('REPLIERS_KEY')
API_ENDPOINT = 'https://api.repliers.io/listings'

# Configure Google Gemini API Key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')

    # Chat with Gemini AI
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat_session = model.start_chat(history=[])
    ai_response = chat_session.send_message(user_input)

    # Check if user input asks for property details and call REPLIERS API
    if "property" in user_input.lower():
        # Assume filters are extracted from the user input (e.g., number of bedrooms, price range)
        listings = get_property_listings(min_price=100000, max_price=500000, num_bedrooms=3)  # Example hardcoded filters
        return jsonify({
            'response': ai_response.text,
            'listings': listings  # Include property listings in response
        })
    
    # Default response if no property query is detected
    return jsonify({'response': ai_response.text})

def get_property_listings(min_price, max_price, num_bedrooms):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "REPLIERS-API-KEY": API_KEY
    }

    params = {
        'minPrice': min_price,
        'maxPrice': max_price,
        'numBedrooms': num_bedrooms,
        'hasImages': True
    }

    result_fields = ("address.*,map.*,mlsNumber,listPrice,originalPrice,images[1],"
                     "details.numBedrooms,details.numBathrooms,details.sqft,"
                     "details.numGarageSpaces,details.propertyType,details.garage,lastStatus,lot.,resource")

    api_url = f'{API_ENDPOINT}?fields={result_fields}'

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()  # Return the fetched listings
    except requests.RequestException as e:
        return {'error': f'Failed to fetch listings. Error: {str(e)}'}

if __name__ == '__main__':
    app.run(debug=True)
