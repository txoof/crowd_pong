
# coding: utf-8

# In[52]:

# HSV Sampling
import cv2
import numpy as np

class colorHSV:
    #class that contains high and low values for Hue, Saturation, Value
    def __init__(self, hue, sat, val, lower):
        self.hue = hue
        self.sat = sat
        self.val = val
        self.lower = lower
        
# accept the value slider and pass the result to the HSV variable
def adjust(x):
    pass

def camInit(videoDev):
    return(cv2.VideoCapture(videoDev))

def main():
    #setup colors
    colorA=colorHSV([0,255], [0,255], [0,255])
    colorB=colorHSV([0,255], [0,255], [0,255])
    print colorA.hue, colorB.hue
    
    #define video device
    videoDev=0
    
    #start camera
    cap=camInit(videoDev)
    
    #capture each frame
    _, frame = cap.read()
    #convert captured frame into HSV color space
    hsv=cv2.cvtCo(frame, cv2.COLOR_BGR2HSV)
    
    maskA=cv2.inRange(hsv, colorA)
    
    
    
    


# In[53]:

main()


# In[ ]:



