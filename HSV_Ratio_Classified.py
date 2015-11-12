
# coding: utf-8

# In[15]:

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
    
    def __init__(self, videoDev = 0, frameWidth = 500):
        '''create a frame object that holds all of the frame, hsv frame and mask data for a filter
        videoDev - numeration for video capture device; 0 is default
        frameWidth - width in px of video capture; 500 is default
        frame - cv2.VideoCapture(<video device>)
        name - human readable name for refference 
        hsvFrame - frame converted into HSV space
        mask - a mask calculated based on properties passed
        result - the result of a bitwise_and of the frame and the mask
        
        '''
        self.cap = cv2.VideoCapture(videoDev, frameWidth)
        #_, self.frame = self.cap.read()
        self.frame = self.readFrame()
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.mask = self.calcMask()
        self.result = self.calcRes()
    
    # ideally this should update the HSV frame as well.  Don't know how to make that happen
    def readFrame(self, width = 500):
        '''update the stored frame from the video capture device'''
        #_, self.frame = self.cap.read() 
        _, tempFrame= self.cap.read()
        r = float(width) / tempFrame.shape[1]
        dim = (int(width), int(tempFrame.shape[0] * r))
        resizedFrame = cv2.resize(tempFrame, dim, interpolation = cv2.INTER_AREA)
        self.frame = resizedFrame
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
        self.nonZero = cv2.countNonZero(self.mask)
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

# add branch to detect "out of range"
def updateControlWindow(name, midBGRcolor, colorRange='' ):
    '''update the control pannel windows with color swatches and text'''
    img = colorSwatch(swatchColor = midBGRcolor)
    if midBGRcolor == (0, 0, 0):
        img = addText(img, text = 'Hue + < Hue - OUT OF RANGE!')
    else:
        img = addText(img, textColor = (255, 255, 255), text = 'Aproximate middle color of hue range')
        img = addText(img, textColor = (255, 255, 255), text = 'Color range: ' + colorRange, position = (10, 50))
        img = addText(img, textColor = (255, 255, 255), text = name, position = (10, 75))
    cv2.imshow(name, img)
    #return img

def ratio(countA, countB):
    if countA==countB:
        return(0)
    if countA > countB:
        # give a negative number
        percent=-1*((countA-countB)/float(countA))
    if countA < countB:
        #give a positve number
        percent=1*((countB-countA)/float(countB))
    return(percent)


# In[28]:

# init variables

# color channels
colorA = colorHSV('UP - Green')
colorB = colorHSV('DOWN - Violet')
channels = [colorA, colorB]

# video stream device
videoDev = 0
# live frame object
myFrame = cvFrame(0)
#pixel count
pixelCount = {}
masks = {}

# default settings
pause = False
displayOff = False

# init trackbars for each channel
for color in channels:
    color.createTrackBars()
    updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])
    
# begin looping until user quits
while True: 
  
    # capture key presses & act on them
    keyPress = cv2.waitKey(1)
    # pause live display, destroy windows, display pause message
    if keyPress & 0xFF == ord ('p'):
        pause = True
        displayOff = True
    # quit and cleanup    
    if keyPress & 0xFF == ord ('Q'):
        print 'we out.'
        break
    # unpause     
    if keyPress & 0xFF == ord ('u'):
        pause = False
        displayOff = False
    #reset the keypress variable
    keyPress=False    
    
    # check for changes in trackbar
    # update control panels and color swatches
    # update live frame 
    # calculate the mask for each channel
    
    # capture a frame and convert to HSV space
    myFrame.readFrame()
    myFrame.cvtHSV()
    
    # loop over each channel
    for color in channels:
        changes = False
        #make a copy of the color object for checking later 
        oldColor = color.copy()
        # check with the openCV HighGUI for changes on the trackbars
        color.syncTrackBars()
        
        # if the color range slider has moved update the hue range and the sliders
        if oldColor.colorRange != color.colorRange:
            color.setRangeDefault()
            cv2.setTrackbarPos(color.sliderHue[0], color.controlWinName, color.defaultRanges[color.colorRange][0])
            cv2.setTrackbarPos(color.sliderHue[1], color.controlWinName, color.defaultRanges[color.colorRange][1])
            changes=True
        
        # if the hue sliders have moved, update color swatch
        if (oldColor.lower[0] != color.lower[0]) or (oldColor.upper[0] != color.upper[0]):
            changes=True
        
        # update the windows if only if things have changed
        if changes:
            # update the color swatch attached to each control window
            updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])
            
        # calculate the masks and pixel count 
        masks[color.name] = myFrame.calcMask(color.lower, color.upper)
        pixelCount[color.name] = myFrame.nonZero
    
    # calculate the ratio of colors in terms of a value between -1 and 1
    outputValue = ratio(pixelCount[colorA.name], pixelCount[colorB.name])
    print outputValue
    
    # pause live updating and destroy some windows to save memory
    if pause and displayOff:
        pauseFrame = myFrame.frame
        # destroy unneeded windows
        for color in channels:
            cv2.destroyWindow(color.name)
        # add pause text to live window
        addText(pauseFrame, 'Live display paused (calculations continue).')
        addText(pauseFrame, 'Press and hold "u" to unpause.', position = (10, 50))
        addText(pauseFrame, 'Hold "shift+q" to quit.', position = (10, 100))
        cv2.imshow('Live', pauseFrame)
        # unset pause condition
        pause = False       
   
    # calculate the resultant image for each channel
    # display live, result channels or pause message
    if not displayOff:
        # FIXME! Hack that does not use the class
        # I can't figure out how to do this using the class methods I have built.  
        # I would rather display each result frame from within a for loop like everything else
        # Unfortunately the mask is not recorded in the object so the last mask that is calculated
        # is saved and the result is based on ONLY that structure.
        resA = cv2.bitwise_and(myFrame.frame, myFrame.frame, mask = masks[colorA.name])
        addText(resA, text = 'lower: ' + str(colorA.lower))
        addText(resA, text = 'upper: ' + str(colorA.upper), position = (10, 50))
        resB = cv2.bitwise_and(myFrame.frame, myFrame.frame, mask = masks[colorB.name])
        addText(resB, text = 'lower: ' + str(colorB.lower))
        addText(resB, text = 'upper: ' + str(colorB.upper), position = (10, 50))
        cv2.imshow(colorA.name, resA)
        cv2.imshow(colorB.name, resB)
           addText(myFrame.frame, text = str(outputValue))
        cv2.imshow('Live', myFrame.frame)

    
# destroy all windows
myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)    


# In[26]:

myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[10]:

a = 500
a = a + 0.0
print type(a)
print a, int(a)


# In[ ]:

colorA = colorHSV('UP - green')
colorB = colorHSV('DOWN - violet')

#video device
videoDev = 0
# control default display output
displayOff = False   
# create a fame capture object
myFrame = cvFrame(0)
#pixel count variable
count = {}

# recurse each of the set colors and create trackbars
for color in [colorA, colorB]:
    color.createTrackBars()
    updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])
    
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
            displayOff = False
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

    
    #this is kind of broken, the mask is recalculated for each loop, but not saved
    
    # update the mask and pixel count each cycle
    for color in [colorA, colorB]:
        # update the mask
        myFrame.calcMask(color.lower, color.upper)
        count[color.name] = myFrame.nonZero
    
    # destroy undeeded windows & display a message when display has been paused
    if displayOff and pause:
        pauseFrame = myFrame.frame
        for color in [colorA, colorB]:
            cv2.destroyWindow(color.name)
        # add text to live window
        addText(pauseFrame, 'Live display paused (calculations continue).')
        addText(pauseFrame, 'Press and hold "u" to unpause.', position = (10, 50))
        addText(pauseFrame, 'Hold "shift+q" to quit.', position = (10, 100))
        cv2.imshow('Live', pauseFrame)
        # unset pause condition
        pause = False
    
    if not displayOff:
        # update the captured frame every round
        myFrame.readFrame()
        myFrame.cvtHSV()
        # show the live frame with added text
        addText(myFrame.frame, text = 'raw pixel count: ' 
                + str(count[colorA.name]) + ':' + str(count[colorB.name]))
        cv2.imshow('Live', myFrame.frame)
        for color in [colorA, colorB]:
            # update the result frame
            myFrame.calcRes()
            # add relevant information to frame
            addText(myFrame.result, text = 'lower: ' + str(color.lower))
            addText(myFrame.result, text = 'upper: ' + str(color.upper), position = (10, 60))
            # show the result frame
            cv2.imshow(color.name, myFrame.result)
     
    
myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:

myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[14]:

a=500

print type(float(a))


# In[ ]:

prin

