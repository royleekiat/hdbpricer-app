import math
#import tensorflow as tf
from collections import defaultdict
import numpy as np
from numpy import unique
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
#from tensorflow import keras
#from tensorflow.keras import layers
#import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from sklearn.neighbors import KNeighborsRegressor
import pickle

def train():
    #Dataset from https://data.gov.sg/dataset/resale-flat-prices
    file_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8OfO82KXoRmO0E6c58MdwsOSc8ns5Geme87SiaiqTUrS_hI8u8mYE5KIOfQe4m2m3GGf9En22xuXx/pub?gid=382289391&single=true&output=csv"
    data = pd.read_csv(file_url)

    dataframe = data.copy()

    #let's break date to years, months
    dataframe['date'] = pd.to_datetime(dataframe['month'])
    dataframe['month'] = dataframe['date'].apply(lambda date:date.month)
    dataframe['year'] = dataframe['date'].apply(lambda date:date.year)

    #Get number of years left on lease as a continuous number (ignoring months)
    dataframe['remaining_lease'] = dataframe['remaining_lease'].apply(lambda remaining_lease:remaining_lease[:2])

    #Get storey range as a continuous number
    dataframe['storey_range'] = dataframe['storey_range'].apply(lambda storey_range:storey_range[:2])

    #Concat address
    dataframe['address'] = dataframe['block'].map(str) + ', ' + dataframe['street_name'].map(str) + ', Singapore' 

    '''
    #Geocode by address
    locator = Nominatim(user_agent="myGeocoder")

    # 1 - convenient function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # 2- - create location column
    dataframe['location'] = dataframe['address'].apply(geocode)
    print("step 2")
    # 3 - create longitude, laatitude and altitude from location column (returns tuple)
    dataframe['point'] = dataframe['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    print("step 3")
    # 4 - split point column into latitude, longitude and altitude columns
    dataframe[['latitude', 'longitude', 'altitude']] = pd.DataFrame(dataframe['point'].tolist(), index=df.index)
    print("step 4")
    '''
    #Geocode by town (Singapore is so small that geocoding by addresses might not make much difference compared to geocoding to town)
    town = [x for x in dataframe['town'].unique().tolist() 
                if type(x) == str]
    latitude = []
    longitude =  []
    for i in range(0, len(town)):
        # remove things that does not seem usefull here
        try:
            geolocator = Nominatim(user_agent="ny_explorer")
            loc = geolocator.geocode(town[i])
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
            #print('The geographical coordinate of location are {}, {}.'.format(loc.latitude, loc.longitude))
        except:
            # in the case the geolocator does not work, then add nan element to list
            # to keep the right size
            latitude.append(np.nan)
            longitude.append(np.nan)
    # create a dataframe with the locatio, latitude and longitude
    df_ = pd.DataFrame({'town':town, 
                        'latitude': latitude,
                        'longitude':longitude})
    # merge on Restaurant_Location with rest_df to get the column 
    dataframe = dataframe.merge(df_, on='town', how='left')

    ### label encode the categorical values and convert them to numbers 
    '''
    le = LabelEncoder()

    dataframe['town']= le.fit_transform(dataframe['town'].astype(str))

    dataframe['flat_type'] = le.fit_transform(dataframe['flat_type'].astype(str))

    dataframe['street_name'] = le.fit_transform(dataframe['street_name'].astype(str))

    #dataframe['storey_range'] = le.fit_transform(dataframe['storey_range'].astype(str))

    dataframe['flat_model'] = le.fit_transform(dataframe['flat_model'].astype(str))

    dataframe['block'] = le.fit_transform(dataframe['block'].astype(str))

    dataframe['address'] = le.fit_transform(dataframe['address'].astype(str))
    '''

    townDict = {'ANG MO KIO': 1,'BEDOK': 2,'BISHAN': 3,'BUKIT BATOK': 4,'BUKIT MERAH': 5,'BUKIT PANJANG': 6,'BUKIT TIMAH': 7,'CENTRAL AREA': 8,'CHOA CHU KANG': 9,'CLEMENTI': 10,'GEYLANG': 11,'HOUGANG': 12,'JURONG EAST': 13,'JURONG WEST': 14,'KALLANG/WHAMPOA': 15,'MARINE PARADE': 16,'PASIR RIS': 17,'PUNGGOL': 18,'QUEENSTOWN': 19,'SEMBAWANG': 20,'SENGKANG': 21,'SERANGOON': 22,'TAMPINES': 23,'TOA PAYOH': 24,'WOODLANDS': 25,'YISHUN': 26,}
    flat_typeDict = {'1 ROOM': 1,'2 ROOM': 2,'3 ROOM': 3,'4 ROOM': 4,'5 ROOM': 5,'EXECUTIVE': 6,'MULTI-GENERATION': 7,}


    dataframe['town'] = dataframe['town'].replace(townDict, regex=True)
    dataframe['flat_type'] = dataframe['flat_type'].replace(flat_typeDict, regex=True)

    # drop some unnecessary columns
    dataframe = dataframe.drop('date',axis=1)

    dataframe = dataframe.drop('block',axis=1)
    #dataframe = dataframe.drop('lease_commence_date',axis=1)
    dataframe = dataframe.drop('month',axis=1)
    dataframe = dataframe.drop('street_name',axis=1)
    dataframe = dataframe.drop('address',axis=1)
    dataframe = dataframe.drop('flat_model',axis=1)
    #dataframe = dataframe.drop('town',axis=1)
    dataframe = dataframe.drop('year',axis=1)
    #dataframe = dataframe.drop('latitude',axis=1)
    dataframe = dataframe.drop('remaining_lease',axis=1)


    X = dataframe.drop('resale_price',axis =1)
    y = dataframe['resale_price']
    X=X.values
    y=y.values
    #splitting Train and Test 
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    #standardization scaler - fit&transform on train, fit only on test

    s_scaler = StandardScaler()
    X_train = s_scaler.fit_transform(X_train.astype(np.float))
    X_test = s_scaler.transform(X_test.astype(np.float))

    knn = KNeighborsRegressor(algorithm='brute')

    knn.fit(X_train,y_train)

    #save model
    filename = 'hdbknn.sav'
    scalername = 'scaler.sav'
    pickle.dump(knn, open(filename, 'wb'))
    pickle.dump(s_scaler, open(scalername, 'wb'))

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.score(X_test, y_test)
    print(result)
    return result


