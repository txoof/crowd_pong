
# coding: utf-8

# In[26]:

import cv2
import numpy as np
import re
import copy


# In[36]:

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
            
        # default color range
        self.setRangeDefault()
#        self.lower = self.setHSVvalues( [ self.defaultRanges[self.colorRange][0],
#                                        self.satRange[0], self.valRange[0]] )
#        self.upper = self.setHSVvalues( [self.defaultRanges[self.colorRange][1], 
#                                        self.satRange[1], self.valRange[1]] )
#        self.lower = self.setHSVvalues([self.hueRange[0], self.satRange[0], self.valRange[0]])
#        self.upper = self.setHSVvalues([self.hueRange[1], self.satRange[1], self.valRange[1]])
    
    def setRangeDefault(self):
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
        print self.name, self.lower, self.upper, midBGRcolor
        return int(midBGRcolor[0][0][0]), int(midBGRcolor[0][0][1]), int(midBGRcolor[0][0][2])

        
    def copy(self):
        '''make a duplicate object'''
        return copy.deepcopy(self)
    
    def hasChanged(self):
        '''compare self to a copy and if it has changed'''
        pass

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
    img = addText(img, textColor = (255, 255, 255), text = colorRange, position = (10, 50))
    img = addText(img, textColor = (255, 255, 255), text = name, position = (10, 75))
    cv2.imshow(name, img)
    #return img


# In[38]:

colorA = colorHSV('UP - green')
colorB = colorHSV('DOWN - violet')
# recurse each of the set colors and create trackbars
for color in [colorA, colorB]:
    color.createTrackBars()
    updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])

while True:
    

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
        # something is broken with the calculation of the mid point - upper slider does not work
        if (oldColor.lower[0] != color.lower[0]) or (oldColor.upper[0] != color.upper[0]):
            changes=True
        
        if changes:
            # update the color swatch
            updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])

        
        
    if cv2.waitKey(1) & 0xFF == ord('Q'): 
            print 'we out.'
            break
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[35]:

print colorA.defaultRanges
print colorA.colorRange
print colorA.lower
print colorA.upper
print colorB.colorRange
print colorB.lower
print colorB.upper


# In[ ]:



