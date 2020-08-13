#!/usr/bin/env python
# coding: utf-8

import HexToWeights
import json
import sys
import cv2
import base64
import requests
import datetime
from urllib.parse import urlencode

#takes in the image name as the first command
path = sys.argv[1]
image = cv2.imread(path)

client_id ='979a863072334960959d826594c0d65d'
client_secret = #client secret goes here!


# declare class
class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_client_credentials(self):
        """
        returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
        
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Couldn't auth client")
        data = r.json()
        now = datetime.datetime.now() #gives me the time the request happens
        access_token = data['access_token']
        expires_in = data['expires_in'] #seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now #bool to say if expired   
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        return headers
    
    def get_resource(self, lookup_id,resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def get_tracks(self, _id):
        return self.get_resource(_id, resource_type='tracks')
    
    def search(self, query, search_type='artist'): #keep in mind type is a python operator
        access_token = self.get_access_token()
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}" #need the question mark
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
        #takes in integer w weight from 1 to 10    
    def wTrack(self, w):
        _id = 0
        if w == 1:
            #Numb by Linkin Park
            _id = "2nLtzopw4rPReszdYBJU6h"
        if w == 2:
            #Bakamitai - Taxi driver edition
            _id = "4xXu9UO2qdBotUOfqru2UC"
        if w == 3:
            #Time by Pink Floyd
            _id = "3TO7bbrUKrOSPGRTB5MeCz"
        if w == 4:
            #Mr. Brightside by the Killers
            _id = "3dho80fD9LVp471UuFHEEr"
        if w == 5:
            #She Was Mine by AJ Rafael
            _id = "6NV8bM1StHDcWMoTVWix1J"
        if w == 6:
            #Kiss me by Pixpence None the richer
            _id = "2kyezitNXSQaIa1nsQRWVp"
        if w == 7:
            #Kodachrome by Paul Simon
            _id = "3f0U5NaD1bCk8nmKpn2ZJY"
        if w == 8:
            #Wouldn't It be Nice by the Beach Boys
            _id = "2Gy7qnDwt8Z3MNxqat4CsK"
        if w == 9:
            #Don't Go Breaking my heart by Elton John
            _id = "5pKJtX4wBeby9qIfFhyOJj"
        if w == 10:
            #Caramelldansen
            _id = "7MwwPyZJ7UKFROj2oVnH6R"      
        return self.get_tracks(_id)

#this function calls the function in HexToWeights
#takes in the path
#returns back the weight
def getWeight(image):
    pixelArr = HexToWeights.getRGB(image)
    HSVArr = HexToWeights.getHSV(pixelArr)
    return HexToWeights.getWeight(HSVArr)

spotify = SpotifyAPI(client_id, client_secret)
#spotify.search("Caramelldansen", search_type="track")

#spotify.get_artist("6XyY86QOPPrYVGvF9ch6wz")

#spotify.get_tracks("2nLtzopw4rPReszdYBJU6h")
w = getWeight(image)
outF = open("json_output.txt", "w")
output = spotify.wTrack(w)
json.dump(output, outF)
outF.close()





