
import numpy as py
import cv2
from collections import Counter

#testing image path
path = './test.jpg'
image = cv2.imread(path)

#class of pixel
class Pixel():

    #initialize itself
    def __init__(self):
        #RGB
        self.R = 0
        self.G = 0
        self.B = 0
        #HSV
        self.H = 0 #Hue
        self.S = 0 #Saturation
        self.V = 0 #Value

    def getR(self, R):
        self.R = R
    def getG(self, G):
        self.G = G
    def getB(self, B):
        self.B = B

    def R(self):
        return self.R
    def G(self):
        return self.G
    def B(self):
        return self.B


    def getH(self, H):
        self.H = H
    def getS(self, S):
        self.S = S
    def getV(self, V):
        self.V = V

    def H(self):
        return self.H
    def S(self):
        return self.S
    def V(self):
        return self.V

#takes "in" an image and iterates over every pixel
#and returns an array of pixel objects
def getRGB(image):
    pixelArr = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #new pixel object
            newPixel = Pixel()
            #image[i,j] returns the BRG value of that pixel
            newPixel.getR(image[i,j][2])
            newPixel.getG(image[i,j][1])
            newPixel.getB(image[i,j][0])
            #append new pixel object to pixelArr
            pixelArr.append(newPixel)
    return pixelArr

#takes in an array of pixel objects
#and defines its HSV values
def getHSV(pixelArr):
    averageH = []
    averageS = []
    averageV = []
    HSVArr = []
    for i in pixelArr:
        rPrime = i.R/255
        gPrime = i.G/255
        bPrime = i.B/255

        cMax = max(rPrime, gPrime, bPrime)
        cMin = min(rPrime, gPrime, bPrime)
        delta = cMax - cMin

        H = 0
        S = 0
        V = 0
        
        #hue calculation
        if delta == 0:
            H = 0
        elif cMax == rPrime:
            H = (60)*(((gPrime-bPrime)/delta)%6)
        elif cMax == gPrime:
            H = (60)*(((bPrime-rPrime)/delta)+2)
        elif cMax == bPrime:
            H = (60)*(((rPrime-gPrime)/delta)+4)

        #saturation calculation:
        if cMax == 0:
            S = 0
        else:
            S = delta/cMax

        #value calculation:
        V = cMax

        #set the HSV values into the pixelArr
        i.getH(H)
        i.getS(S)
        i.getV(V)

        #add it to the average
        averageH.append(H)
        averageS.append(S)
        averageV.append(V)

    #how many values
    num = 10
    #get the most common HSV values
    averageH = Counter(averageH)
    averageS = Counter(averageS)
    averageV = Counter(averageV)
    #then put those values into the array
    averageH = averageH.most_common(num)
    averageS = averageS.most_common(num)
    averageV = averageV.most_common(num)
    #put those values into pixels
    for i in range(num):
        newPixel = Pixel()
        #get the HSV values
        newPixel.getH(averageH[i][0])
        newPixel.getS(averageS[i][0])
        newPixel.getV(averageV[i][0])
        #append new pixel object to pixelArr
        HSVArr.append(newPixel)
    #return the arry of most common pixels    
    return HSVArr


#takes in the averageHSV array, which is 3(?) most common pixels/colors
#returns a weight of 1 (sad), 2 (vibe), 3 (happy)
def getWeight(HSVArr):
    weight = 0
    totalPixels = len(HSVArr)
    aveH = 0
    aveS = 0
    aveV = 0
    for i in range(totalPixels):
        aveH += HSVArr[i].H
        aveS += HSVArr[i].S
        aveV += HSVArr[i].V
    aveH = aveH/totalPixels
    aveS = aveS/totalPixels
    aveV = aveV/totalPixels
    print(aveH, aveS, aveV)
    if aveV <= .2 and aveS <= .4:
        weight = 1 #dramatic and slow
    elif aveV <= .2 and aveS <= .8:
        weight = 2 #angry and slow
    elif aveV <= .4 and aveS >= .8 and aveS <= 1:
        weight = 3 #angry and fast
    elif aveV <= .4 and aveS >= .2 and aveS <= .8:
        weight = 4 #sad boi hours
    elif aveV <= .8 and aveS <= .2:
        weight = 5 #kinda chill sad
    elif aveV <= .8 and aveS <= .4:
        weight = 6 #vibing lofi
    elif aveV <= .6 and aveS <= 1:
        weight = 7 #crooners?
    elif aveV <= .8 and aveS <= 1:
        weight = 8 #pop/pop rock
    elif aveV <= 1 and aveS <= .6:
        weight = 9 #intense pop/pop rap?/happy rock?
    else:
        weight = 10 #super fast dance music
        
    print(weight)    
    return weight
           
pixelArr = getRGB(image)
HSVArr = getHSV(pixelArr)
getWeight(HSVArr)
