from math import log
from Tkinter import Tk
from tkFileDialog import *
import csv
import png

H = 500
iterations = 30
ColorList = []

#Majority of processing work completed here.
#Calculates how close a point is to the mandelbrot set
def mandelbrot(real, imag):
        z = complex(0,0)
        c = complex(real, imag)
        dropOutLevel = 0
        for i in range(0, iterations):
                if abs(z) < 2:
                        z = z**2 + c
                        dropOutLevel += 1
                else:
                        break

        z = z**2 + c
        z = z**2 + c
        z = z**2 + c
        z = z**2 + c
        return dropOutLevel,z

#Interpolates (Smooths) between 2 different colours
def interpolateC(color,endColor,left):
        if left == 0:
                return color
        rStart = color[0]
        gStart = color[1]
        bStart = color[2]
        rEnd = endColor[0]
        gEnd = endColor[1]
        bEnd = endColor[2]
        rDiff = rEnd-rStart
        gDiff = gEnd-gStart
        bDiff = bEnd-bStart
        rInc = float(rDiff)/left
        gInc = float(gDiff)/left
        bInc = float(bDiff)/left
        #print (str(left))
        return [rStart+rInc,gStart+gInc,bStart+bInc]

#Reads colour stops from a file chosen by the user using the tkinter library
def getPoints():
        Tk().withdraw()
        filename = askopenfilename()
        reader = csv.reader(open(filename, "rb"), delimiter=',')
        pointsList = []
        for row in reader:
                colorList = []
                for a in row:
                        colorList.append(float(a)/255)
                pointsList.append(colorList)

        backwards = pointsList[0:-1]
        backwards.reverse()
        return pointsList+backwards

#Gets the location to save the file
def getSaveLocation():
        Tk().withdraw()
        savefile = asksaveasfilename(defaultextension='.png')
        return savefile

#Sets up a list of colours for the rendering to use from the points file
def colorList():
        cols = []
        points = getPoints()
        eachLength = H/(len(points)-1)
        howmanytogo = eachLength
        
        for a in range(1,len(points)):
                cols.append(points[a-1])
                for i in range (0,eachLength):
                        cols.append(interpolateC(cols[-1],points[a],howmanytogo))
                        howmanytogo += -1


                howmanytogo = eachLength
        global ColorList
        ColorList = cols

#Turns a number into a colour for the renderer to display
def toColor(a):
        a=a*85
        a = int(a)%H
        try:
                a = ColorList[int(a)]
                return [int(a[0]*255),int(a[1]*255), int(a[2]*255)]
        except IndexError:
                print a
                print len(ColorList)
                return [0,0,0]

def v(z,n):
        try:
                x = n + 1 - log(log(abs(z),2),2)/log(2,2)
                return x
        except ValueError:
                print(str(z))
        return 0

def heightVals(pixSize, t, b, pixH):
        hList = []
        locCount = t-pixSize/2
        while locCount>b:
                hList.append(locCount)
                locCount -= pixSize
        if pixH == len(hList):
                return hList
        else:
                print "oh dear... something's gone wrong", hList, t, b, locCount


def widthVals(pixSize, l, r, pixW):
        wList = []
        locCount = l+pixSize/2
        while locCount<r:
                wList.append(locCount)
                locCount += pixSize
        if pixW == len(wList):
                return wList
        else:
                print "oh dear... something's gone wrong", wList, r, l, locCount

colorList()
saveFile = getSaveLocation()
w = int(raw_input("Width in pixels:"))
h = int(raw_input("Height in pixels:"))
x = float(raw_input("X position:"))
y = float(raw_input("Y position:"))
zoom = float(raw_input("Zoom level:"))

#at zoom level 1, 1 pixel is 
ratio = 100
pixelSize = float(1)/float(ratio)/zoom
left = x-((w/2)*pixelSize)
right = x+((w/2)*pixelSize)
top = y+((h/2)*pixelSize)
bottom = y-((h/2)*pixelSize)
print pixelSize,left,right,top,bottom
#1/(100/zoomLevel)
wVals = widthVals(pixelSize, left, right,w)
hVals = heightVals(pixelSize, top, bottom,h)

mainArray = []



for a in hVals:
        rowArray = []
        for b in wVals:
                n, z = mandelbrot(b,a)
                if (n == iterations):
                        col = [0,0,0]
                else:
                        col = toColor(v(z,n))
                rowArray = rowArray + col
                #print n, z, col
        mainArray.append(rowArray)
        

f = open(saveFile, 'wb')
w = png.Writer(w, h)
w.write(f, mainArray)
f.close()
