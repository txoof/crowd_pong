
# coding: utf-8

# In[1]:

import cv2
import numpy as np
import re
import copy

#Classes
class colorHSV:
    '''Form a range of values for HSV colorspace filtering based on color:
    
    name -- a user readable name that includes one of the color ranges 
            such as: 'Color One - red'
    colorRange -- select from a predefined color range (default is 0)
    
        pre defined color ranges in terms of Hue (0-179)
        
        Range Number - human name - Hue Range
        0            - full       - 0-179
        1            - red        - 0-35
        2            - yellow     - 25-65
        3            - green      - 55-95
        4            - blue       - 85-125
        5            - indigo     - 115-155
        6            - violet     - 145-179
    '''
    # class attributes
    defaultRanges = [[0, 179, 'full'], [0, 35, 'red'], [25, 65, 'yellow'], [55, 95, 'green'], 
                     [85, 125, 'blue'], [115, 155, 'indigo'], [145, 179, 'violet']]
   
    # maximum and minimum values for Hue, Sat, Val
    hueRange = [0, 179]
    satRange = [0, 255]
    valRange = [0, 255]
    
    # track bar attributes
    sliderHue = ['Hue-', 'Hue+']
    sliderSat = ['S-', 'S+']
    sliderVal = ['V-', 'V+']
    sliderColRange = ['ColorRange']

    #sliderHue = ['Hue-', 'Hue+']
    #sliderSat = ['S-', 'S+']
    #sliderVal = ['V-', 'V+']
    #sliderColRange = ['CR']
    
    
    
    def __init__(self, name='default', colorRange=0):
        '''Init an HSV Color Range object consiting of a 3 element numpy.array
            lower -- lower end of color space range for filtering
            upper -- upper end of color space range for filtering
            colorRange -- one of the predefined color ranges; -1 by default
            controlWinName - name for reffering to an openCV HighGUI window
        '''
        #Attributes
        self.name = name

        # set the name for a control slider window
        self.controlWinName = self.name + '_controls'
        
        
        # integer loop counter
        iC=0
        
        # temporarily set self.colorRange to false
        self.colorRange = False
        for i in self.defaultRanges:
            # create a regexp for finding the human readable color range in the name
            regexp = self.defaultRanges[iC][2] + '.*'
            # search the color name against the names in defaultRanges
            m = re.search(regexp, self.name, re.IGNORECASE)
            
            # if a match has been made
            if m is not None:
                # set the color range equal to the loop counter
                self.colorRange=iC
                #stop looking here
                break
            
            #increment the counter
            iC += 1
        # if a range name was not found, set the range to 0: full
        if not self.colorRange:
            self.colorRange = colorRange
            
        # set to default color range
        self.setRangeDefault()
    
    def setRangeDefault(self):
        '''use the predefined defaults to set hue range'''
        self.lower = self.setHSVvalues( [ self.defaultRanges[self.colorRange][0],
                                        self.satRange[0], self.valRange[0]] )
        self.upper = self.setHSVvalues( [self.defaultRanges[self.colorRange][1], 
                                        self.satRange[1], self.valRange[1]] )
    
    def setHSVvalues(self, hsv = np.array( [0, 0, 0] )):
        '''sets a list of values as type numpy.array()'''
        return np.array(hsv)
    
    
    def createTrackBars(self):
        '''Create openCV HighGUI trackbars in a window that matches name + _contorls'''
        
        # create a named window to attach everything to
        cv2.namedWindow(self.controlWinName)
        
        # Hue Sliders
        cv2.createTrackbar(self.sliderHue[0], self.controlWinName,
                          self.lower[0], self.hueRange[1], adjust)
        cv2.createTrackbar(self.sliderHue[1], self.controlWinName,
                          self.upper[0], self.hueRange[1], adjust)
        
        # saturation sliders
        cv2.createTrackbar(self.sliderSat[0], self.controlWinName, 
                          self.lower[1], self.satRange[1], adjust)
        #cv2.createTrackbar(self.sliderSat[1], self.controlWinName, 
        #                 self.upper[1], self.satRange[1], adjust)
        
        # value sliders
        cv2.createTrackbar(self.sliderVal[0], self.controlWinName, 
                          self.lower[2], self.valRange[1], adjust)
        cv2.createTrackbar(self.sliderVal[1], self.controlWinName,
                          self.upper[2], self.valRange[1], adjust)
        
        cv2.createTrackbar(self.sliderColRange[0], self.controlWinName,
                          self.colorRange, len(self.defaultRanges)-1, adjust)
        
    def syncTrackBars(self):
        '''record the position of openCV trackbars in lower and upper'''

        #hue
        self.lower[0] = cv2.getTrackbarPos(self.sliderHue[0], self.controlWinName)

        self.upper[0] = cv2.getTrackbarPos(self.sliderHue[1],self.controlWinName)

        #saturation
        self.lower[1] = cv2.getTrackbarPos(self.sliderSat[0], self.controlWinName)
        # currently unused
        #self.upper[1] = cv2.getTrackbarPos(self.sliderSatat[1], self.controlWinName)

        #value
        self.lower[2] = cv2.getTrackbarPos(self.sliderVal[0], self.controlWinName)
        self.upper[2] = cv2.getTrackbarPos(self.sliderVal[1], self.controlWinName)

        #color range
        self.colorRange = cv2.getTrackbarPos(self.sliderColRange[0], self.controlWinName)

    def midBGRcolor(self):
        '''return the middle value between the upper and lower hue values in BGR space'''
        colorDelta=(self.upper[0] - self.lower[0])
        # negative values don't make sense, set them to 0
        if colorDelta < 0:
            midHSVcolor = np.uint8([[[0, 0, 0]]])
        else:    
            midHSVcolor = np.uint8([[[self.lower[0] + (colorDelta)//2, 255, 255]]])
        midBGRcolor = cv2.cvtColor(midHSVcolor, cv2.COLOR_HSV2BGR)
        return int(midBGRcolor[0][0][0]), int(midBGRcolor[0][0][1]), int(midBGRcolor[0][0][2])

        
    def copy(self):
        '''make a duplicate object'''
        return copy.deepcopy(self)
    
    # Ask martin about this again
    def hasChanged(self):
        '''compare self to a copy and if it has changed'''
        pass

class cvFrame:
    
    def __init__(self, videoDev = 0):
        '''create a frame object that holds all of the frame, hsv frame and mask data for a filter
        frame - cv2.VideoCapture(<video device>)
        name - human readable name for refference 
        hsvFrame - frame converted into HSV space
        mask - a mask calculated based on properties passed
        '''
        self.cap = cv2.VideoCapture(videoDev)
        #_, self.frame = self.cap.read()
        self.frame = self.readFrame()
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.mask = self.calcMask()
        self.result = self.calcRes()
    
    # ideally this should update the HSV frame as well.  Don't know how to make that happen
    def readFrame(self):
        '''update the stored frame from the video capture device'''
        _, self.frame = self.cap.read() 
        return self.frame
        
    def cvtHSV(self):
        '''create an HSV version of the frame'''
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        return self.hsvFrame
        
    def release(self):
        '''release the video capture device'''
        self.cap.release()
    
    def calcMask(self, lower = np.array( [0, 0, 0] ), upper = np.array( [179, 255, 255] )):
        '''calculate a mask based on two np.array objects with HSV values'''
        self.mask = cv2.inRange(self.hsvFrame, lower, upper, )
        return self.mask
    
    def calcRes(self):
        self.result = cv2.bitwise_and(self.frame, self.frame, mask = self.mask)
        return self.result
    
def adjust(x):
    pass

def addText(img, text = 'your text here', position = (10, 25), 
            textColor = (0, 255, 0)):
    '''Add text to an openCV image'''
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.putText(img, text, position, font, 1.25, textColor, 2)
    return img

def colorSwatch(swatchColor = (255, 0, 255), xDim = 800, yDim = 100):
    img = np.zeros((yDim, xDim, 3), np.uint8)
    cv2.rectangle(img, (0, 0), (xDim, yDim), swatchColor, -1) 
    return img

 
def updateControlWindow(name, midBGRcolor, colorRange='' ):
    img = colorSwatch(swatchColor = midBGRcolor)
    img = addText(img, textColor = (255, 255, 255), text = 'aproximate middle of hue range')
    img = addText(img, textColor = (255, 255, 255), text = 'color range: ' + colorRange, position = (10, 50))
    img = addText(img, textColor = (255, 255, 255), text = name, position = (10, 75))
    cv2.imshow(name, img)
    #return img


# In[4]:

colorA = colorHSV('UP - green')
colorB = colorHSV('DOWN - violet')

#video device
videoDev = 0
# create a fame capture varaible
#capFrame = cv2.VideoCapture(videoDev)
myFrame = cvFrame(0)

# recurse each of the set colors and create trackbars
for color in [colorA, colorB]:
    color.createTrackBars()
    updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])
# control display output
displayOff = False    

while True:
   
    # capture key presses and do stuff
    keyPress = cv2.waitKey(1)
    if keyPress:
        if keyPress & 0xFF == ord ('p'):
            print 'pause!'
            pause = True
            displayOff = True
            
        if keyPress & 0xFF == ord ('Q'):
            print 'we out.'
            break
            
        if keyPress & 0xFF == ord ('u'):
            print 'unpause!'
            pause = False
            
        keyPress=False
    
    
    for color in [colorA, colorB]:
        changes = False
        #make a copy of each color object for checking later
        oldColor = color.copy()
        color.syncTrackBars()
        
        # if the color range slider has moved update the hue range and the sliders
        if oldColor.colorRange != color.colorRange:
            color.setRangeDefault()
            cv2.setTrackbarPos(color.sliderHue[0], color.controlWinName, color.defaultRanges[color.colorRange][0])
            cv2.setTrackbarPos(color.sliderHue[1], color.controlWinName, color.defaultRanges[color.colorRange][1])
            changes=True
        
        # if the HSV sliders have moved, update color swatch
        if (oldColor.lower[0] != color.lower[0]) or (oldColor.upper[0] != color.upper[0]):
            changes=True
        
        if changes:
            # update the color swatch
            updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])


    
    # update the mask and resultant frame each cycle
    for color in [colorA, colorB]:
        # update the mask
        myFrame.calcMask(color.lower, color.upper)
    
    # destroy undeeded windows when display has been paused
    if displayOff and pause:
        pauseFrame = myFrame.frame
        for color in [colorA, colorB]:
            cv2.destroyWindow(color.name)
        # add text to live window
        addText(pauseFrame, 'Live display paused (calculations continue).')
        addText(pauseFrame, 'Press and hold "u" to unpause.', position = (10, 50))
        addText(pauseFrame, 'Hold "shift+q" to quit.', position = (10, 100))
        cv2.imshow('Live', pauseFrame)
    
    if not displayOff:
        # update the captured frame every round
        myFrame.readFrame()
        myFrame.cvtHSV()
        # show the live frame
        cv2.imshow('Live', myFrame.frame)
        for color in [colorA, colorB]:
            # update the result frame
            myFrame.calcRes()
            # show the result frame
            cv2.imshow(color.name, myFrame.result)

    
myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:




# In[ ]:



