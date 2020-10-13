from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from predict import predictPrice


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

HDBs = [
    {
        'town': 'ANG MO KIO',
        'flat_type': '2 ROOM',
        'storey_range': '10 TO 12',
        'floor_area_sqm': 44.0,
        'lease_commence_date': 1979,
        'resale_price': 232000.0,

    },

    #town, flat_type,storey_range,floor_area_sqm,lease_commence_date
]

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/hdbs', methods=['GET', 'POST'])
def all_hdbs():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        HDBs.append({
            'town': post_data.get('town'),
            'flat_type': post_data.get('flat_type'),
            'storey_range': post_data.get('storey_range'),
            'floor_area_sqm': post_data.get('floor_area_sqm'),
            'lease_commence_date': post_data.get('lease_commence_date'),
            'resale_price': round(predictPrice( town = post_data.get('town'),flat_type=post_data.get('flat_type'),storey_range=post_data.get('storey_range'),floor_area_sqm=post_data.get('floor_area_sqm'),lease_commence_date=post_data.get('lease_commence_date'))*1.01), # To return from model
        })
        response_object['message'] = 'Priced!'
    else:
        response_object['hdbs'] = HDBs
    return jsonify(response_object)



if __name__ == '__main__':
    app.run()