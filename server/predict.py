import math
#import tensorflow as tf
from collections import defaultdict
import numpy as np
from numpy import unique
import pandas as pd
from sklearn.preprocessing import StandardScaler
#from tensorflow import keras
#from tensorflow.keras import layers
#import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from sklearn.neighbors import KNeighborsRegressor
import pickle

def predictPrice(town,flat_type,storey_range,floor_area_sqm,lease_commence_date):
    
    #town, flat_type,storey_range,floor_area_sqm,lease_commence_date
    input_data = {
        'town': town,
        'flat_type': flat_type,
        'storey_range': storey_range,
        'floor_area_sqm': floor_area_sqm,
        'lease_commence_date': lease_commence_date,
    }
    

    #Geocode by town (Singapore is so small that geocoding by addresses might not make much difference compared to geocoding to town)
    town = input_data["town"]
    latitude = 0
    longitude =  0
    try:
        geolocator = Nominatim(user_agent="ny_explorer")
        loc = geolocator.geocode(town)
        latitude= loc.latitude
        longitude = loc.longitude
        #print('The geographical coordinate of location are {}, {}.'.format(loc.latitude, loc.longitude))
    except:
        # in the case the geolocator does not work, then add nan element
        # to keep the right size
        latitude = np.nan
        longitude = np.nan
    input_data['latitude'] = latitude
    input_data['longitude'] = longitude
    input_data['storey_range'] = input_data['storey_range'][:2]

    townDict = {'ANG MO KIO': 1,'BEDOK': 2,'BISHAN': 3,'BUKIT BATOK': 4,'BUKIT MERAH': 5,'BUKIT PANJANG': 6,'BUKIT TIMAH': 7,'CENTRAL AREA': 8,'CHOA CHU KANG': 9,'CLEMENTI': 10,'GEYLANG': 11,'HOUGANG': 12,'JURONG EAST': 13,'JURONG WEST': 14,'KALLANG/WHAMPOA': 15,'MARINE PARADE': 16,'PASIR RIS': 17,'PUNGGOL': 18,'QUEENSTOWN': 19,'SEMBAWANG': 20,'SENGKANG': 21,'SERANGOON': 22,'TAMPINES': 23,'TOA PAYOH': 24,'WOODLANDS': 25,'YISHUN': 26,}
    flat_typeDict = {'1 ROOM': 1,'2 ROOM': 2,'3 ROOM': 3,'4 ROOM': 4,'5 ROOM': 5,'EXECUTIVE': 6,'MULTI-GENERATION': 7,}

    input_data['town'] = townDict[input_data['town']]
    input_data['flat_type'] = flat_typeDict[input_data['flat_type']]

    dataframe = pd.DataFrame.from_records([input_data])
    data = dataframe.values

    scalername = 'scaler.sav'
    s_scaler = pickle.load(open(scalername, 'rb'))
    data = s_scaler.transform(data.astype(np.float))

    #print(data)

    filename = 'hdbknn.sav'

    loaded_model = pickle.load(open(filename, 'rb'))

    result = loaded_model.predict(data)
    #print(result)
    return result[0]