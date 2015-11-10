
# coding: utf-8

# In[1]:

#HSV Sampling of video feed

import cv2
import numpy as np
import re
import copy

#Classes
class colorHSV:
    # Attributes
    colorSpace = 'HSV-180'
    # preset color ranges
    defaultRanges = [[0, 35, 'red'], [25, 65, 'yellow'], [55, 95, 'green'], 
                     [85, 125, 'blue'], [115, 155, 'indigo'], [145, 179, 'violet']]
    # maximum and minimum values for Hue, Sat, Val
    hueRange = [0,179]
    satRange = [0, 255]
    valRange = [0, 255]
    
    def __init__(self, name='default', colorRange = 0):
        '''
        Return an HSV Color Range Object
        '''
        #Attributes
        self.name = name
        # set the default color range
        self.lower = np.array( [0, 0, 0] )
        self.upper = np.array( [179, 0, 0])
    
    def createTrackBars(self):
        '''
        Create openCV trackbars with names matching the color
        '''
        #Initialize trackbars
        # Attributes
        self.controlWinName = self.name + '_controls'
        
        self.sliderHue = ['Hue-', 'Hue+']
        self.sliderSat = ['S-', 'S+']
        self.sliderVal = ['V-', 'V+']
        self.sliderColRange = ['CR']
        
        # create a named window for the controls
        cv2.namedWindow(self.controlWinName)
        
        #Variables
        # integer loop counter
        iC = 0
        
        # Attributes
        # set colorRange equal to -1 in the event that nothing is found
        self.colorRange = -1
        # set default lower and upper values for Hue, Saturation, Value (HSV)
        self.lower = np.array([self.hueRange[0], self.satRange[0], self.valRange[0]])
        self.upper = np.array([self.hueRange[1], self.satRange[1], self.valRange[1]])
        
        for i in self.defaultRanges:
            # create a regexp to match color names - pull the name from the default ranges list
            regexp=self.defaultRanges[iC][2] + '.*'
            m = re.search(regexp, self.name, re.IGNORECASE)
            # set colorRange to the position in the default range list
            if m is not None:
                # set the color range equal to the loop counter
                self.colorRange = iC
                # stop looking here
                break
            iC += 1        
        
        # set initial HSV values
        # set the range wide open if one of the defaults was not found via searching self.name
        if self.colorRange < 0:
            self.lower = np.array([self.hueRange[0], self.satRange[0], self.valRange[0]])
            self.upper = np.array([self.hueRange[1], self.satRange[1], self.valRange[1]])
        else:
            self.lower = np.array([self.defaultRanges[self.colorRange][0], self.hueRange[0], self.hueRange[0]])
            self.upper = np.array([self.defaultRanges[self.colorRange][1], self.hueRange[1], self.hueRange[1]])    
        
        # Hue sliders
        cv2.createTrackbar(self.sliderHue[0], self.controlWinName, self.lower[0], self.hueRange[1], adjust)
        cv2.createTrackbar(self.sliderHue[1], self.controlWinName, self.upper[0], self.hueRange[1], adjust)
        
        # Saturation slider(s)
        # in practice only a lower end slider is needed
        cv2.createTrackbar(self.sliderSat[0], self.controlWinName, self.lower[1], self.satRange[1], adjust)
        
        # Value sliders
        # in practice only a lower end slider is needed
        cv2.createTrackbar(self.sliderVal[0], self.controlWinName, self.lower[2], self.valRange[1], adjust)
        
        # Color range slider
        cv2.createTrackbar(self.sliderColRange[0], self.controlWinName, self.colorRange, len(self.defaultRanges) - 1, adjust)
        

        # MOVED this to main loop, doesn't seem like something the class should be doing
        # add a colored box that matches the middle value of the color range
        # lower+abs(lower-upper)//2
        #midHSVcolor = np.uint8([[[self.lower[0] + abs(self.lower[0] - self.upper[0])//2, 255, 255]]])
        #midBGRcolor = cv2.cvtColor(midHSVcolor, cv2.COLOR_HSV2BGR)
        #bgrVal = (int(midBGRcolor[0][0][0]), int(midBGRcolor[0][0][1]), int(midBGRcolor[0][0][2]))
        #cv2.imshow(self.controlWinName, colorImg(yDim = 100, color = bgrVal))


    def syncTracBars(self):
        # record the position of the track bars
        #HUE
        self.lower[0] = self.hueRange[0] + cv2.getTrackbarPos(self.sliderHue[0], self.controlWinName)
        self.upper[0] = self.hueRange[0] + cv2.getTrackbarPos(self.sliderHue[1], self.controlWinName)
        
        #SAT
        self.lower[1] = self.satRange[0] + cv2.getTrackbarPos(self.sliderSat[0], self.controlWinName)
        #self.upper[1] = self.satRange[0] + cv2.getTrackbarPos(self.sliderSat[1], self.controlWinName)
        
        #VAL
        self.lower[2] = self.valRange[0] + cv2.getTrackbarPos(self.sliderVal[0], self.controlWinName)
        
        #Color Range
        self.colorRange = 0 + cv2.getTrackbarPos(self.sliderColRange[0], self.controlWinName)
    
           
    def clone(self):
        '''make a duplicate object'''
        return copy.deepcopy(self)
    
    def midBGRColor(self):
        '''return the middle value between the upper and lower hue values in BGR space'''
        colorDelta=(self.upper[0] - self.lower[0])
        if colorDelta < 0:
            midHSVcolor = np.uint8([[[0, 0, 0]]])
        else:    
            midHSVcolor = np.uint8([[[self.lower[0] + (self.upper[0] - self.lower[0])//2, 255, 255]]])
        midBGRcolor = cv2.cvtColor(midHSVcolor, cv2.COLOR_HSV2BGR)
        return int(midBGRcolor[0][0][0]), int(midBGRcolor[0][0][1]), int(midBGRcolor[0][0][2])
    
    def calcmask(self, hsvFrame):
        self.hsvFrame = hsvFrame
        self.mask = cv2.inRange(hsvFrame, self.lower, self.upper)
        return self.mask
        
    def calcResult(self, frame):
        self.frame = frame
        self.result = cv2.bitwise_and(self.frame, self.frame, mask=self.calcMask(frame))
        return self.result
        
def colorImg(xDim=800, yDim=100, color=(0, 0, 0) ):
    img=np.zeros((yDim, xDim, 3), np.uint8)
    cv2.rectangle(img, (0,0), (xDim, yDim), color, -1)
    return img
        
def adjust(x):
    pass

def addText(frame, text='Text Goes Here', position=(10,50), textColor=(255, 255, 0)):
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.putText(frame, text, position, font, 2, textColor, 2)
    return(frame)

# fix this later
def colorSwatch(text='your text here', swatchColor=(179, 255, 255), textColor=(0, 0, 0), xDim=100, yDim=100):
    img = colorImg(color=swatchColor, xDim=xDim, yDim=yDim)
    img = addText(img, textColor=textColor, text=text)
    return img

def main():
    #Initialize variables
    
    colorBoxText='mid-point color'
    
    #base glow stick colors (can be adjusted later manually)
    stickA='UP Color - violet'
    stickB='DN Color - green'
    videoDev = 0
    cap = cv2.VideoCapture(videoDev)
    colorA = colorHSV(stickA)
    colorB = colorHSV(stickB)
    
    colorA.createTrackBars()
    colorB.createTrackBars()
    
    
    #### the colored box could probabl be a class too
    # add a colored box that matches the middle value of the color range
    # lower+abs(lower-upper)//2
    for color in [colorA, colorB]:
        colorBox = colorImg(color=color.midBGRColor())
        colorBox = addText(colorBox, textColor = (0, 0, 0), text=colorBoxText)
        cv2.imshow(color.controlWinName, colorBox)  
    
    
    while(1):
        _, frame = cap.read()
        
        # convert frame to HSV
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # consider adding this to the class as a method
        for color in [colorA, colorB]:
            changes=False
            oldColor = color.clone()
            color.syncTracBars()  
            
            # if the color range has changed update the trackbars for the hue
            # this works
            if oldColor.colorRange != color.colorRange:
                color.lower[0]=color.defaultRanges[color.colorRange][0]
                color.upper[0]=color.defaultRanges[color.colorRange][1]  
                cv2.setTrackbarPos(color.sliderHue[0], color.controlWinName, color.defaultRanges[color.colorRange][0])
                cv2.setTrackbarPos(color.sliderHue[1], color.controlWinName, color.defaultRanges[color.colorRange][1])
                changes=True
            

            if (oldColor.lower[0] != color.lower[0]) or (oldColor.upper[0] != color.upper[0]):
                changes=True
            
            
            # only update if there have been changes
            if changes:
                # Deal with the color swatches in the control panels
                colorBox = colorImg(color=color.midBGRColor())
                if color.midBGRColor() == (0, 0, 0):
                    print 'out of range'
                    colorBox = addText(colorBox, textColor = (255, 255, 255), text='out of range')
                else:
                    colorBox = addText(colorBox, textColor = (0, 0, 0), text=colorBoxText)
                cv2.imshow(color.controlWinName, colorBox)

        #calculate the Masks and results
        #maskA=cv2.inRange(hsvFrame, colorA.lower, colorA.upper)
        #maskB=cv2.inRange(hsv, colorB.lower, colorB.upper)
        
        #count non-zero pixels not covered by the mask
        #countA=cv2.countNonZero(maskA)
        #countB=cv2.countNonZero(maskB)
        
        # Display the results
        cv2.imshow('Live', frame)
        cv2.imshow(colorA.name, colorA.calcmask(hsvFrame))
        
        #cv2.imshow(colorA.name, maskA)
        
        # Quit for Shfit+Q (cpaital Q)    
        # Add confirmation here - should not quit immediately
        if cv2.waitKey(1) & 0xFF == ord('Q'): 
            print 'we out.'
            break
            
  

    #release the capture device and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    print 'thanks for playing'
    


# In[2]:

main()


# In[ ]:

def adjust(x):
    pass


img=cv2.imread('IMG_0026.JPG')
cv2.namedWindow('foo')
cv2.createTrackbar('Bar', 'foo', 0, 10, adjust)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:



