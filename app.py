from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# In-memory storage for session data (replace with a database in production)
chat_history = []
property_listings = [
    {   
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": None,
            "country": "Canada",
            "district": "Toronto E05",
            "majorIntersection": " Roneld/nldci MKAvcenye",
            "neighborhood": "L'Amoreaux",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "yedneKn",
            "streetNumber": "3002",
            "streetSuffix": "Rd",
            "unitNumber": None,
            "zip": "4 YV21M"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "Lnda",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "10268.00",
        "map": {
            "latitude": 43.8078605,
            "longitude": -79.3003621,
            "point": "POINT (-79.3003621 43.8078605)"
        },
        "mlsNumber": "E9349520",
        "originalPrice": 5008,
        "resource": "3tPpe1y2r:8ro"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": "09..C100018",
            "country": None,
            "district": "Toronto C08",
            "majorIntersection": "c/egnnohYimRod",
            "neighborhood": "Church-Yonge Corridor",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "mrbodLa",
            "streetNumber": "20",
            "streetSuffix": "St",
            "unitNumber": None,
            "zip": "MA507C "
        },
        "details": {
            "garage": None,
            "numBathrooms": 0,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "rkceLo",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "11985.00",
        "map": {
            "latitude": 43.6516524,
            "longitude": -79.3769603,
            "point": "POINT (-79.3769603 43.6516524)"
        },
        "mlsNumber": "C9310595",
        "originalPrice": 5080,
        "resource": ":rPtr31e28oyp"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": "1.1.0008C90",
            "country": None,
            "district": "Toronto C08",
            "majorIntersection": "igoo neh&n dRYmc",
            "neighborhood": "Church-Yonge Corridor",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "labmdor",
            "streetNumber": "20",
            "streetSuffix": "St",
            "unitNumber": None,
            "zip": "C A750M"
        },
        "details": {
            "garage": None,
            "numBathrooms": 0,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "kecLor",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "6892.00",
        "map": {
            "latitude": 43.6516524,
            "longitude": -79.3769603,
            "point": "POINT (-79.3769603 43.6516524)"
        },
        "mlsNumber": "C9310637",
        "originalPrice": 8050,
        "resource": "1y:3poeP8rt2r"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": "011100.0C.1",
            "country": None,
            "district": "Toronto C01",
            "majorIntersection": "oapdka and FnorStYr i",
            "neighborhood": "Waterfront Communities C1",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "bIcaeto",
            "streetNumber": "51",
            "streetSuffix": "Terr",
            "unitNumber": "RLOCEK",
            "zip": "V 4A55M"
        },
        "details": {
            "garage": None,
            "numBathrooms": 0,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "Locker",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "14480.00",
        "map": {
            "latitude": 43.6405556,
            "longitude": -79.3968958,
            "point": "POINT (-79.3968958 43.6405556)"
        },
        "mlsNumber": "C9308651",
        "originalPrice": 606,
        "resource": "3r18pPtey2o:r"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": "010.1C0.011",
            "country": None,
            "district": "Toronto C01",
            "majorIntersection": "rd SFtp  rnkoaoYndaia",
            "neighborhood": "Waterfront Communities C1",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "teaoIbc",
            "streetNumber": "15",
            "streetSuffix": "Terr",
            "unitNumber": "KLECRO",
            "zip": "55 4VMA"
        },
        "details": {
            "garage": None,
            "numBathrooms": 0,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "oecLrk",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "8059.00",
        "map": {
            "latitude": 43.6405556,
            "longitude": -79.3968958,
            "point": "POINT (-79.3968958 43.6405556)"
        },
        "mlsNumber": "C9308625",
        "originalPrice": 2600,
        "resource": "2yr:ot83Pper1"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Peel",
            "city": "Mississauga",
            "communityCode": None,
            "country": "Canada",
            "district": "Mississauga",
            "majorIntersection": "suvRdaStMia/s nDd ",
            "neighborhood": "Mavis-Erindale",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "leodaWefl",
            "streetNumber": "0538",
            "streetSuffix": "Rd",
            "unitNumber": "Raer",
            "zip": "C 1V58L"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "andL",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "11031.00",
        "map": {
            "latitude": 43.5651688,
            "longitude": -79.6381944,
            "point": "POINT (-79.6381944 43.5651688)"
        },
        "mlsNumber": "W9305552",
        "originalPrice": 7,
        "resource": "8o:tr21yrep3P"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Grey County",
            "city": "Southgate",
            "communityCode": None,
            "country": "Canada",
            "district": "Southgate",
            "majorIntersection": " Hg G8&ohda8air Rw e9yy ",
            "neighborhood": "Rural Southgate",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "S ,guhodRe a8tt",
            "streetNumber": "89762",
            "streetSuffix": None,
            "unitNumber": None,
            "zip": "N1N 00G"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "ramF",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "9014.00",
        "map": {
            "latitude": 44.07170740000001,
            "longitude": -80.4011846,
            "point": "POINT (-80.4011846 44.07170740000001)"
        },
        "mlsNumber": "X9282729",
        "originalPrice": 5600,
        "resource": "petr2o8y:r3P1"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Hamilton",
            "city": "Hamilton",
            "communityCode": None,
            "country": "Canada",
            "district": "Hamilton",
            "majorIntersection": "nSKiht gSttur &   AEr",
            "neighborhood": "Gibson",
            "state": "Ontario",
            "streetDirection": "E",
            "streetDirectionPrefix": None,
            "streetName": "ngiK",
            "streetNumber": "578",
            "streetSuffix": "St",
            "unitNumber": None,
            "zip": "A1M5 L8"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "anLd",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "11182.00",
        "map": {
            "latitude": 43.2512947,
            "longitude": -79.84500349999999,
            "point": "POINT (-79.84500349999999 43.2512947)"
        },
        "mlsNumber": "X9282609",
        "originalPrice": 300,
        "resource": "tP31erpy:or82"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Hamilton",
            "city": "Hamilton",
            "communityCode": "00.0051.07",
            "country": None,
            "district": "Hamilton",
            "majorIntersection": "o ilsonl wyC5 d/HnR",
            "neighborhood": "Rural Flamborough",
            "state": "Ontario",
            "streetDirection": "S",
            "streetDirectionPrefix": None,
            "streetName": "snnoollCi",
            "streetNumber": "785",
            "streetSuffix": "Rd",
            "unitNumber": None,
            "zip": "3HLE95 "
        },
        "details": {
            "garage": None,
            "numBathrooms": 4,
            "numBedrooms": 4,
            "numGarageSpaces": 0,
            "propertyType": "rmaF",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "12600.00",
        "map": {
            "latitude": 43.29107,
            "longitude": -80.01297,
            "point": "POINT (-80.01297 43.29107)"
        },
        "mlsNumber": "X9260680",
        "originalPrice": 5040,
        "resource": "381trPp2oery:"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "York",
            "city": "Vaughan",
            "communityCode": None,
            "country": "Canada",
            "district": "Vaughan",
            "majorIntersection": "   roeelvyrlBEDgviFy/ddlVaulee",
            "neighborhood": "Concord",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "lyValeFrou ",
            "streetNumber": "15",
            "streetSuffix": "Dr",
            "unitNumber": None,
            "zip": "4 4KVL8"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "nadL",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "13504.00",
        "map": {
            "latitude": 43.8145012,
            "longitude": -79.5410685,
            "point": "POINT (-79.5410685 43.8145012)"
        },
        "mlsNumber": "N9256648",
        "originalPrice": 9000,
        "resource": "yrrp1t3P:2o8e"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": None,
            "country": "Canada",
            "district": "Toronto W10",
            "majorIntersection": " yH27w",
            "neighborhood": "West Humber-Clairville",
            "state": "Ontario",
            "streetDirection": "W",
            "streetDirectionPrefix": None,
            "streetName": "letseSe",
            "streetNumber": "9567",
            "streetSuffix": "Ave",
            "unitNumber": "2",
            "zip": " 9R4M9V"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "Lnad",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "7890.00",
        "map": {
            "latitude": 43.7561394,
            "longitude": -79.60893039999999,
            "point": "POINT (-79.60893039999999 43.7561394)"
        },
        "mlsNumber": "W9248253",
        "originalPrice": 52,
        "resource": "ryrep:t23P81o"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Halton",
            "city": "Milton",
            "communityCode": None,
            "country": "Canada",
            "district": "Milton",
            "majorIntersection": "s LnrweLht8an/ ie oiBLee ",
            "neighborhood": "Trafalgar",
            "state": "Ontario",
            "streetDirection": "E",
            "streetDirectionPrefix": None,
            "streetName": "arw BeLsoe",
            "streetNumber": "2301",
            "streetSuffix": "Line",
            "unitNumber": None,
            "zip": "39SLT 5"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "daLn",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "11376.00",
        "map": {
            "latitude": 43.4894265,
            "longitude": -79.7825407,
            "point": "POINT (-79.7825407 43.4894265)"
        },
        "mlsNumber": "W9245869",
        "originalPrice": 5080,
        "resource": "o2P:t8ep3rry1"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Toronto",
            "city": "Toronto",
            "communityCode": None,
            "country": "Canada",
            "district": "Toronto W01",
            "majorIntersection": "tdnne se eulosN abQ t",
            "neighborhood": "Roncesvalles",
            "state": "Ontario",
            "streetDirection": "W",
            "streetDirectionPrefix": None,
            "streetName": "eQuen",
            "streetNumber": "0213",
            "streetSuffix": "St",
            "unitNumber": None,
            "zip": "61LM K4"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "aLnd",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "11048.00",
        "map": {
            "latitude": 43.6419265,
            "longitude": -79.4308155,
            "point": "POINT (-79.4308155 43.6419265)"
        },
        "mlsNumber": "W9245372",
        "originalPrice": 80,
        "resource": "prt:3Py1eo28r"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "York",
            "city": "Whitchurch-Stouffville",
            "communityCode": None,
            "country": "Canada",
            "district": "Whitchurch-Stouffville",
            "majorIntersection": "/rr8y4Aa udr do HwS",
            "neighborhood": "Ballantrae",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "h48gayHwi ",
            "streetNumber": "01151",
            "streetSuffix": None,
            "unitNumber": None,
            "zip": "47 L3AX"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "nLda",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "10804.00",
        "map": {
            "latitude": 44.0342754,
            "longitude": -79.29596620000001,
            "point": "POINT (-79.29596620000001 44.0342754)"
        },
        "mlsNumber": "N9239852",
        "originalPrice": 3520,
        "resource": "8:or3pet2rP1y"
    },
    {
       'filters': {'bedrooms': 3, 'bathrooms': 2},
        "address": {
            "area": "Simcoe",
            "city": "New Tecumseth",
            "communityCode": None,
            "country": "Canada",
            "district": "New Tecumseth",
            "majorIntersection": "aR gayi ttdeHe t9oh oThWm wsnf",
            "neighborhood": "Tottenham",
            "state": "Ontario",
            "streetDirection": None,
            "streetDirectionPrefix": None,
            "streetName": "gwyHi9 ha",
            "streetNumber": "6829",
            "streetSuffix": None,
            "unitNumber": None,
            "zip": "00G W1L"
        },
        "details": {
            "garage": None,
            "numBathrooms": None,
            "numBedrooms": None,
            "numGarageSpaces": None,
            "propertyType": "anLd",
            "sqft": None
        },
        "images": [
            "sandbox/IMG-SANDBOX_1.jpg",
            "sandbox/IMG-SANDBOX_2.jpg",
            "sandbox/IMG-SANDBOX_3.jpg",
            "sandbox/IMG-SANDBOX_4.jpg",
            "sandbox/IMG-SANDBOX_5.jpg"
        ],
        "lastStatus": "New",
        "listPrice": "12716.00",
        "map": {
            "latitude": 43.9823475,
            "longitude": -79.8120331,
            "point": "POINT (-79.8120331 43.9823475)"
        },
        "mlsNumber": "N9235476",
        "originalPrice": 5,
        "resource": "tr8P1yp:e23or"
    }
]

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    chat_history.append({'role': 'user', 'content': user_message})

    # Here you would typically call your AI model to get a response
    # For demonstration, we'll simulate a simple response
    assistant_response = f"You said: {user_message}"  # Replace with AI response logic
    chat_history.append({'role': 'assistant', 'content': assistant_response})

    return jsonify({
        'chatresponse': assistant_response,
        'property_listings': property_listings,  # Include property listings if needed
        'arguments': [property['filters'] for property in property_listings]
    })

@app.route('/clear-session', methods=['GET'])
def clear_session():
    global chat_history
    chat_history = []  # Clear chat history
    return jsonify({'status': 'success', 'message': 'Chat history cleared.'})

@app.route('/filteredlistings', methods=['POST'])
def filtered_listings():
    filters = request.json
    filtered_properties = [p for p in property_listings if all(p['filters'].get(k) == v for k, v in filters.items())]
    return jsonify(filtered_properties)

if __name__ == '__main__':
    app.run(debug=True)
