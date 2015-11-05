
# coding: utf-8

# In[39]:

# HSV Sampling
import cv2
import numpy as np

class colorHSV:
    #class that contains high and low values for Hue, Saturation, Value
    def __init__(self, name, hue, sat, val):
        self.name = name
        self.hue = hue
        self.sat = sat
        self.val = val
        self.lower=np.array([hue[0], sat[0], val[0]])
        self.upper=np.array([hue[1], sat[1], val[1]])
        
# accept the value slider and pass the result to the HSV variable
def adjust(x):
    pass

def camInit(videoDev):
    return(cv2.VideoCapture(videoDev))

#def slidersHSV(color):
    
def createTrackbar(color):
    cv2.createTrackbar('Hue_upper', color.name, color.hue[1], abs(color.hue[1]-color.hue[0]), adjust)
    
def main():
    
    #setup colors
    colorA=colorHSV('red',[0,255], [0,255], [0,255])
    colorB=colorHSV('green',[0,255], [0,255], [0,255])

    
    #define video device
    videoDev=0
    
    #start camera
    cap=camInit(videoDev)
    
    createTrackbar(colorA)
    
    while(1):
        #capture each frame
        _, frame = cap.read()
    
        #convert captured frame into HSV color space
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #Calculate mask
        maskA=cv2.inRange(hsv, colorA.lower, colorA.upper)
        maskB=cv2.inRange(hsv, colorB.lower, colorB.upper)
    
        #Caluclate result (bitwise and of mask and frame)
        resA=cv2.bitwise_and(frame, frame, mask=maskA)
        resB=cv2.bitwise_and(frame, frame, mask=maskB)
    
        #show live and colorA and colorB feed
        cv2.imshow('Live', frame)
        cv2.imshow('ColorA', maskA)
        cv2.imshow('ColorB', resB)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    print 'thanks for playing'


# In[40]:

main()


# In[ ]:




# In[ ]:



