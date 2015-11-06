
# coding: utf-8

# In[4]:

# HSV Sampling
import cv2
import numpy as np


# Classes
class colorHSV:
    #class that contains high and low values for Hue, Saturation, Value
    # name: 'Human referenceable name of the color'
    # hue: [minimum value, maximum value]
    # sat: [minimum value, maximum value]
    # val: [minimum value, maximum value]
    # lower: numpy array containing lowest interactively set [H, S, V]
    # upper: numpy array containing hightest interactively set [H, S, V]
    # build names for trackbars
    
    # DO NOT change these trackbar names; 
    # in the OSX OpenCV/QT/Py2.7 environment the trackbar order is effected by the characters in the name!
    # Hue
    hn='Hue'
    # Saturation
    sn='S'
    # Value
    vn='V'
    # Lower and Upper names
    low='-'
    upp='+'
    
    #color range values and names
    values=[[0, 35, 'red'], [25, 65, 'yellow'], [55, 95, 'green'], [85, 125, 'blue'], [115, 155, 'indigo'], [145, 179, 'violet']]
    hueName=(hn+low, hn+upp)
    satName=(sn+low, sn+upp)
    valName=(vn+low, vn+upp)
    
    def __init__(self, name, hue, sat, val):
        self.hue = hue
        self.sat= sat
        self.val =val
        self.name = name
        self.controlName=name+'_win'
        self.colorRange=0
        self.lower=np.array([hue[0], sat[0], val[0]])
        self.upper=np.array([hue[1], sat[1], val[1]])
        
# Helper Subs
def adjust(x):
    # accept the value slider and pass the result to the HSV variable
    pass

def camInit(videoDev):
    return(cv2.VideoCapture(videoDev))

    
def initTrackbars(color):
    #initialize trackbars to window defineid by color.name
    
    #set the default position in the range list
    colorPosition=0
    counter=0
    #Default hue positions
    lowerHue=color.hue[0]
    upperHue=color.hue[1]

    # create a named window that matches the name specified in the variable
    # names that match the defined colors will trigger that color to be chosen at startup
    cv2.namedWindow(color.controlName, flags=cv2.cv.CV_WINDOW_NORMAL)
    for i in color.values:
        if color.name in i:
            colorPosition=counter
            color.colorRange=colorPosition
            lowerHue=i[0]
            upperHue=i[1]
            break
        counter=counter+1
       
    # There is a bizzare bug in this version of opencv that makes the trackbars appear in an 
    # order that depends on the track bar name.  I cannot determine the pattern, but this
    # naming system does work for the moment
    
    #color range control bar
    #FIXME if the name changes of the trackbar, this breaks
    cv2.createTrackbar('CR', color.controlName, colorPosition, len(color.values)-1, adjust)
    
    #Lower Saturation
    cv2.createTrackbar(color.satName[0], color.controlName, color.sat[0], abs(color.sat[1]-color.sat[0]), adjust)
    
    #Upper Hue
    cv2.createTrackbar(color.hueName[1], color.controlName, upperHue, abs(color.hue[1]-color.hue[0]), adjust)    
    #Lower Hue
    cv2.createTrackbar(color.hueName[0], color.controlName, lowerHue, abs(color.hue[1]-color.hue[0]), adjust)
    
    #Lower Value
    cv2.createTrackbar(color.valName[0], color.controlName, color.val[0], abs(color.val[1]-color.val[0]), adjust)
             
    cv2.resizeWindow(color.controlName, 800, 200)

def readTrackbar(color):
    oldColorRange=color.colorRange
    #read the trackbar and pass back changes
    # add the slider value to the pre-defined low end of the color
    # [0:H, 1:S, 2:V] 
    color.lower[0]=color.hue[0]+cv2.getTrackbarPos(color.hueName[0], color.controlName)
    color.upper[0]=color.hue[0]+cv2.getTrackbarPos(color.hueName[1], color.controlName)
    color.lower[1]=color.sat[0]+cv2.getTrackbarPos(color.satName[0], color.controlName)
    color.lower[2]=color.val[0]+cv2.getTrackbarPos(color.valName[0], color.controlName)
    #FIXME if the name changes, this breaks
    color.colorRange=cv2.getTrackbarPos('CR', color.controlName)
    if color.colorRange != oldColorRange:
        color.lower[0]=color.values[color.colorRange][0]
        color.upper[0]=color.values[color.colorRange][1]
        cv2.setTrackbarPos(color.hueName[1], color.controlName, color.values[color.colorRange][1])
        cv2.setTrackbarPos(color.hueName[0], color.controlName, color.values[color.colorRange][0])

    return(color)

def addText(frame, text='Text Goes Here', position=(10,50), textColor=(255, 255, 0)):
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.putText(frame, text, position, font, 2, textColor, 2)
    return(frame)



# In[9]:



def main():

    #VARIABLE DEFS
    
    # window titles and preset name
    # Choose from red, yellow, green, blue, indigo, violet to activate a preset.  
    # Names not in the list above will default to "red", but can be tuned by hand
    stickA='violet'
    stickB='green'
    
    # define video device
    videoDev=0

    # setup color objects
    # Move the HSV ranges into the class - this does not need to be user set.
    colorA=colorHSV(stickA, [0,179], [0,255], [0,255])
    colorB=colorHSV(stickB, [0,179], [0,255], [0,255])
  
    # start camera
    cap=camInit(videoDev)
    
    # initialize the trackbars
    initTrackbars(colorA)
    initTrackbars(colorB)
    
    #FIXME find a way to resize windows dynamically - try rescaling for optimization
    cv2.namedWindow(stickA, flags=cv2.cv.CV_WINDOW_NORMAL)
    cv2.namedWindow(stickB, flags=cv2.cv.CV_WINDOW_NORMAL)
    cv2.namedWindow('Live', flags=cv2.cv.CV_WINDOW_NORMAL)
    
    #set the display on initially
    displayOff=False
    pause=False
    
    while(1):
        #capture each frame
        _, frame = cap.read()
    
        # convert captured frame into HSV color space
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #Read the trackbar positions
        colorA=readTrackbar(colorA)
        colorB=readTrackbar(colorB)
       
       
        # Calculate mask 
        maskA=cv2.inRange(hsv, colorA.lower, colorA.upper)
        maskB=cv2.inRange(hsv, colorB.lower, colorB.upper)
        
        # The mask zeros everything outside of the set range
        # Count everything non-zero for each mask
        countA=cv2.countNonZero(maskA)
        countB=cv2.countNonZero(maskB)  

        #capture keyboard input 
        
        # pause for p key
        #FIXME this needs to be debounced
        if cv2.waitKey(1) & 0xFF == ord('p'):
            displayOff=True
            pause=True
        
        # unpause for u key
        if cv2.waitKey(1) & 0xFF == ord ('u'):
            displayOff=False

        # Quit for Shfit+Q (cpaital Q)    
        # Add confirmation here - should not quit immediately
        if cv2.waitKey(1) & 0xFF == ord('Q'): 
            print 'we out.'
            break
        
        # Stop updating windows
        if displayOff and pause:
            # Destroying windows saves a bit of memory
            cv2.destroyWindow(colorA.name)
            cv2.destroyWindow(colorB.name)
            #cv2.destroyWindow('Live')
            addText(frame, 'Live display paused (calculations continue).')
            addText(frame, 'Press and hold "u" to unpause.', position=(10,100))
            addText(frame, 'Hold "shift+q" to quit', position=(10,150))
            cv2.imshow('Live', frame)
            cv2.waitKey(1)
            pause=False
        
        if not displayOff:
            # Calculate result (bitwise and of mask and frame) 
            # this adds an extra calculation; remove this and stick with just the masks for
            # a bit of extra speed
            resA=cv2.bitwise_and(frame, frame, mask=maskA)
            resB=cv2.bitwise_and(frame, frame, mask=maskB)
            #Pausing the display drops processor usage from ~80% to 30%
            #Display HSV Values
            addText(resA, text='Low: '+str(colorA.lower), position=(10,50))
            addText(resA, text='Upp: '+str(colorA.upper), position=(10,100))
            addText(resB, text='Low: '+str(colorB.lower), position=(10,50))
            addText(resB, text='Upp: '+str(colorB.upper), position=(10,100))
            
            #addText(maskA, text='Low: '+str(colorA.lower), position=(10,50))
            #addText(maskA, text='Upp: '+str(colorA.upper), position=(10,100))
            #addText(maskB, text='Low: '+str(colorB.lower), position=(10,50))
            #addText(maskB, text='Upp: '+str(colorB.upper), position=(10,100))

            # current color range setting
            addText(resA, text='Color Range: '+colorA.values[colorA.colorRange][2], position=(10, 150))
            addText(resB, text='Color Range: '+colorB.values[colorB.colorRange][2], position=(10, 150))

            # current pixel count and ratio
            colorAText=colorA.values[colorA.colorRange][2]+": "+str(countA)
            colorBText=colorB.values[colorB.colorRange][2]+": "+str(countB)
            addText(resA, text=colorAText+" to "+colorBText, position=(10, 200))
            addText(resB, text=colorAText+" to "+colorBText, position=(10, 200))
        
            cv2.imshow('Live', frame)
            cv2.imshow(colorA.name, resA)
            cv2.imshow(colorB.name, resB)
            #cv2.imshow(colorA.name, maskA)
            #cv2.imshow(colorB.name, maskB)
        
        pause=False
               
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    print 'thanks for playing'


# In[10]:

main()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:

# TODO
'''
    Figure out how to read and adjust CV_CAP_PROP_BRIGHTNESS, 
    http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
    make it more difficult to quit 
    add ratio calculations b - a / b or a - b / a  where the denominator is always the smaller number
    display red:green ratio as colors somehow
    add web socket
    clean up directory of cruft
'''


# In[ ]:

A=2
B=3
D=A*1.0
C=B/D
print C
print float(A)/float(B)


# In[ ]:




# In[ ]:



