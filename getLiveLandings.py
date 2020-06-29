#!/usr/bin/python3

import time
import sys
import json
import requests
import argparse
import datetime
from math import radians, cos, sin, asin, sqrt

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return time.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

# Get distance between two positions in km
def haversine(lat1, lng1, lat2, lng2):
    # convert lat long to radians
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # Haversine formula
    dLng = lng2 - lng1
    dLat = lat2 - lat1

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLng / 2) ** 2
    c = 2 * asin(sqrt(a))

    # the earths radius in Km
    radius = 6371

    return c * radius


# Get Arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('lat',
                       metavar='la',
                       type=float,
                       help="The Latitude of home location e.g. 47.3387486"
                       )

argParser.add_argument('long',
                       metavar='ln',
                       type=float,
                       help="The Longitude of home location e.g. 13.6326257"
                       )

argParser.add_argument('distance',
                       metavar='d',
                       type=int,
                       help='The max distance from home in km'
                       )

args = argParser.parse_args()

home = {'latitude': args.lat, 'longitude':  args.long}

# url for manifest containing landing predictions
ManifestURL = 'https://legacy-snus.habhub.org/tracker/get_predictions.php'

# send GET request for JSON
vehicles = requests.get(ManifestURL).json()

#print(len(vehicles))
#print(vehicles)

# Build list of near-by landings
output = ""
for vehicle in vehicles:

    #print(type(vehicle))
    #print(vehicle['vehicle'])
    #print(vehicle)
    # Get the list of predicted future locations for the vehicle
    locationsStr = vehicle['data']
    #print(type(locationsStr))
    locations = json.loads(locationsStr)
    #print(type(locations))

    # Get the last predicted location
    try: 
        landing = locations[-1]
    except:
        #print("Error: No locations predicted for this vehicle:", file=sys.stderr)
        #print(vehicle, file=sys.stderr) 
        continue
    #print(landing)
    #print(type(landing))

    landingDist = haversine(home['latitude'], home['longitude'], float(landing['lat']), float(landing['lon']))

    #print("Name: {}, Distance {:2.0f}km".format(vehicle['vehicle'],landingDist))

    if landingDist <= args.distance:
        #print(int(landing['time']) - time.time())
        landingTimeDiff = abs(int(landing['time']) - time.time())
        if landingTimeDiff < 86400:

#            landingTimeStr = time.strftime('%a %d %H:%M', time.localtime(int(landing['time'])))
            landingTime = time.localtime(int(landing['time']))
            landingTimeStr = (time.strftime('%a %d', landingTime)
                             + suffix(int(time.strftime('%d', landingTime)))
                             + " at " 
                             + time.strftime('%H:%M', time.localtime(int(landing['time']))))

            confidence = vehicle['descending'] + vehicle['landed']

            output += "Name: {}, Confidence {}, Distance {:2.0f}km, Landing: {}, https://www.google.com/maps/dir/{:2.6f},{:2.6f}/{:2.6f},{:2.6f}\n\r".format(
                       vehicle['vehicle'], 
                       confidence, 
                       landingDist,
                       landingTimeStr,
                       home['latitude'], home['longitude'],
                       float(landing['lat']), float(landing['lon']))

# If any landings were in range output these
if len(output) > 0:
    print('Predictions for within {:d}km of home out of {:d} total predictions. \n\r'.format(args.distance, len(vehicles)))
    print(output)

