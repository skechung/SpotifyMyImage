from jinja2 import Environment,FileSystemLoader
import requests
import HexToWeights
import my_spotify_client
import os
import sys
import webbrowser
import json
from flask import Flask,render_template,request

client_id ='30d402e9b7a8414d82da0ffe3135c610'
client_secret = 'cd255070e8614c53aa0529156bf1d8b0'

LaunchPage = Flask(__name__)

@LaunchPage.route('/')
def index():
    return render_template('InputPage.html')

@LaunchPage.route('/',methods=['POST'])
#Post when u want to send data to the server, GET is when you want to get data from server 
def runMainPage():
    #We have the userImage from the submission
    userImage = request.form['UserImage'] 
    #Passes the image through for processing
    passImage = my_spotify_client.getImageProperly(userImage)
    #Creates Spotify Obj
    mySpotifyObj = my_spotify_client.createSpotifyObj(client_id,client_secret)
    #Get's the Images weight
    getWeightImage = my_spotify_client.getWeight(passImage)
    #Creates the jsonFile 
    songInfo = my_spotify_client.createJson(mySpotifyObj,getWeightImage)
    #Parses the info of the jsonFile
    #jsonParser(songInfo)
    parseThrough = json.loads(songInfo)

    return render_template('index.html',song_title,song_artist,user_image)

def jsonParser(jsonFile):
    parseFile = json.loads(jsonFile)
    #We don't actually need to do this
