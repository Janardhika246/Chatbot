from flask import Flask, render_template, request, jsonify
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    ai_response = chat_with_gemini(user_input)

    # Extract filters from user input
    filters = parse_filters(user_input)
    if filters:
        listings = fetch_property_listings(**filters)
        print("Fetched Listings:", listings)  # Debug statement

        if listings and listings.get('listings'):
            listings_with_links = generate_location_links(listings)
            return jsonify({
                'response': ai_response,
                'listings': listings_with_links
            })
        else:
            return jsonify({
                'response': 'No results found. Try another',
                'listings': []
            })

    # Default response if no property query is detected
    return jsonify({'response': ai_response, 'listings': []})

def chat_with_gemini(user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat_session = model.start_chat(history=[])
    ai_response = chat_session.send_message(user_input)
    return ai_response.text

def parse_filters(user_input):
    import re

    filters = {}
    
    # Basic pattern matching (You may need to enhance this)
    price_match = re.search(r'amount\s*should\s*be\s*(\d+)', user_input, re.IGNORECASE)
    bedroom_match = re.search(r'(\d+)\s*bedroom', user_input, re.IGNORECASE)
    bathroom_match = re.search(r'(\d+)\s*bathroom', user_input, re.IGNORECASE)
    city_match = re.search(r'in\s*(\w+)', user_input, re.IGNORECASE)  # Simple city extraction

    if price_match:
        filters['max_price'] = int(price_match.group(1))
    if bedroom_match:
        filters['num_bedrooms'] = int(bedroom_match.group(1))
    if bathroom_match:
        filters['num_bathrooms'] = int(bathroom_match.group(1))
    if city_match:
        filters['city'] = city_match.group(1)

    # Set default values if not provided
    filters.setdefault('min_price', 0)
    filters.setdefault('num_bedrooms', 1)
    filters.setdefault('num_bathrooms', 1)
    
    return filters

def fetch_property_listings(min_price, max_price, num_bedrooms, num_bathrooms, city):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "REPLIERS-API-KEY": API_KEY
    }

    params = {
        'minPrice': min_price,
        'maxPrice': max_price,
        'numBedrooms': num_bedrooms,
        'numBathrooms': num_bathrooms,
        'city': city,
        'hasImages': True
    }

    result_fields = ("address.*,map.*,mlsNumber,listPrice,originalPrice,images[1],"
                     "details.numBedrooms,details.numBathrooms,details.sqft,"
                     "details.numGarageSpaces,details.propertyType,details.garage,"
                     "lastStatus,lot.*,resource")

    api_url = f'{API_ENDPOINT}?fields={result_fields}'

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': f'Failed to fetch listings. Error: {str(e)}'}

def generate_location_links(listings):
    for listing in listings.get('listings', []):
        latitude = listing.get('map', {}).get('latitude')
        longitude = listing.get('map', {}).get('longitude')

        if latitude and longitude:
            listing['location_link'] = f"https://www.google.com/maps?q={latitude},{longitude}"
        else:
            listing['location_link'] = 'Location not available'
    
    return listings

if __name__ == '__main__':
    app.run(debug=True)
