
# coding: utf-8

# In[1]:

import cv2
import numpy as np


# In[2]:

def adjust(x):
    pass
    


# In[3]:

#Adjustment sliders for color range
cv2.namedWindow('red')
#max and min red HSV values (Hue, Saturation Value)
# red appears to occupy 0-30 and 160-180 
minHRed=0
maxHRed=180
minSRed=0
maxSRed=255
minVRed=0
maxVRed=255
#default values
lowerHRedDefault=0
upperHRedDefault=10
# define color ranges in HSV
lower_red = np.array([lowerHRedDefault, minSRed, minVRed])
upper_red = np.array([upperHRedDefault, maxSRed, maxVRed]) 


# create trackbars 
cv2.createTrackbar('Hue_Upper', 'red', upper_red[0], abs(maxHRed-minHRed), adjust)
cv2.createTrackbar('Hue_Lower', 'red', lower_red[0], abs(maxHRed-minHRed), adjust)
cv2.createTrackbar('Sat_Upper', 'red', upper_red[1], abs(maxSRed-minSRed), adjust)
cv2.createTrackbar('Sat_Lower', 'red', lower_red[1], abs(maxSRed-minSRed), adjust)
cv2.createTrackbar('Val_Upper', 'red', upper_red[2], abs(maxVRed-minVRed), adjust)
cv2.createTrackbar('Val_Lower', 'red', lower_red[2], abs(maxVRed-minVRed), adjust)

cv2.namedWindow('green')
minHGreen=40
maxHGreen=80
minSGreen=10
maxSGreen=255
minVGreen=10
maxVGreen=255
#default values
lowerHGreenDefault=50
upperHGreenDefault=70
# define color ranges in HSV
# FIXME multiply by -1 to set initial values; this needs a better solution
lower_green = np.array([lowerHGreenDefault*-1, minSGreen*-1, minVGreen*-1])
upper_green = np.array([upperHGreenDefault, maxSGreen, maxVGreen]) 
print lower_green, upper_green

# create trackbars 
cv2.createTrackbar('Hue_Upper', 'green', upper_green[0], abs(maxHGreen-minHGreen), adjust)
cv2.createTrackbar('Hue_Lower', 'green', lower_green[0], abs(maxHGreen-minHGreen), adjust)
cv2.createTrackbar('Sat_Upper', 'green', upper_green[1], abs(maxSGreen-minSGreen), adjust)
cv2.createTrackbar('Sat_Lower', 'green', lower_green[1], abs(maxSGreen-minSGreen), adjust)
cv2.createTrackbar('Val_Upper', 'green', upper_green[2], abs(maxVGreen-minVGreen), adjust)
cv2.createTrackbar('Val_Lower', 'green', lower_green[2], abs(maxVGreen-minVGreen), adjust)


#minHGreen=50 
#cv2.createTrackbar('lower_green_adjust', 'green', lower_green[0], 79, adjust)
#cv2.createTrackbar('upper_green_adjust', 'green', upper_green[0], 79, adjust)


# In[4]:

cap = cv2.VideoCapture(0)


while(1):
  
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the selected HSV colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    
    
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image
    ratio='Red:Green '+str(cv2.countNonZero(mask_red))+":"+str(cv2.countNonZero(mask_green))
    #res = cv2.bitwise_and(frame,frame, mask= mask_red)
    
    #calculate the resulting image - this may be much slower than just dealing with the masks consider reverting
    res_red=cv2.bitwise_and(frame, frame, mask=mask_red)
    res_green=cv2.bitwise_and(frame, frame, mask=mask_green)
    
    # add red:green ratio to window
    cv2.putText(frame, ratio, (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2 )
    
    # take red:green measurments above this point    
    
    # all text additions need to be made AFTER measurements have been taken!
    # add adjustment slider values to window
    cv2.putText(res_red, "Low:"+str(lower_red), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2 )
    cv2.putText(res_red, "Up: "+str(upper_red), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    #cv2.putText(mask_green, str(lower_green), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2 )
    #cv2.putText(mask_green, str(upper_green), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(res_green, "Low:"+str(lower_green), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2 )
    cv2.putText(res_green, "Up: "+str(upper_green), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    #live image      
    cv2.imshow('live',frame)
    
    #cv2.imshow('red',mask_red)
    cv2.imshow('red', res_red)
    
    #cv2.imshow('green', mask_green )
    cv2.imshow('green', res_green)
    #cv2.imshow('result_green', res_green)
    
    #read and adjust values from sliders
    
    lower_red[0]=minHRed+cv2.getTrackbarPos('Hue_Lower', 'red')
    upper_red[0]=minHRed+cv2.getTrackbarPos('Hue_Upper', 'red')
    lower_red[1]=minSRed+cv2.getTrackbarPos('Sat_Lower', 'red')
    upper_red[1]=minSRed+cv2.getTrackbarPos('Sat_Upper', 'red')
    lower_red[2]=minVRed+cv2.getTrackbarPos('Val_Lower', 'red')
    upper_red[2]=minVRed+cv2.getTrackbarPos('Val_Upper', 'red')

    #FIXME Lower HSV are changed at this point and jump from default values
    # problem is with minHGreen+gtbposition <-
    lower_green[0]=minHGreen+cv2.getTrackbarPos('Hue_Lower', 'green')
    upper_green[0]=minHGreen+cv2.getTrackbarPos('Hue_Upper', 'green')
    lower_green[1]=minSGreen+cv2.getTrackbarPos('Sat_Lower', 'green')
    upper_green[1]=minSGreen+cv2.getTrackbarPos('Sat_Upper', 'green')
    lower_green[2]=minVGreen+cv2.getTrackbarPos('Val_Lower', 'green')
    upper_green[2]=minVGreen+cv2.getTrackbarPos('Val_Upper', 'green')
    #lower_green[0]=cv2.getTrackbarPos('lower_green_adjust', 'green')
    #upper_green[0]=cv2.getTrackbarPos('upper_green_adjust', 'green')
   
     
    #cv2.imshow('res',res)
      

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:




# In[ ]:



