
import numpy as py
import cv2

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
    averageH = 0
    averageS = 0
    averageV = 0
    averageHSV = []
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
        averageH += H
        averageS += S
        averageV += V

    #get the average HSV values
    #then put those values into the array
    totalPixels = len(pixelArr)
    averageH = averageH/totalPixels
    averageHSV.append(averageH)
    averageS = averageS/totalPixels
    averageHSV.append(averageS)
    averageV = averageV/totalPixels
    averageHSV.append(averageV)

    #print(averageHSV)
    return averageHSV


#takes in the averageHSV array
#returns a weight of 1 (sad), 2 (vibe), 3 (happy)
def getWeight(HSVArr):
    weight = 0
    if HSVArr[2] < .4: #V < .4
        weight = 1
    elif HSV[1] < .4: #V >= .4 && S < .4
        weight = 2
    else:
        weight = 3
    print(weight)
    return weight
           
pixelArr = getRGB(image)
HSVArr = getHSV(pixelArr)
getWeight(HSVArr)
