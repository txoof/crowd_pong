
# coding: utf-8

# In[3]:

import cv2
import numpy as np


# In[4]:

def adjust(x):
    pass
    


# In[7]:

#Adjustment sliders for color range
#cv2.namedWindow('red')
#max and min red HSV values (Hue, Saturation Value)
#For typical red objects the hue should be between 155 and 185.  
#Glowsticks will probably need some modifications and testing
'''
minHRed=155
maxHRed=185
minSRed=0
maxSRed=255
minVRed=0
maxVRed=255
#default values
lowerHRedDefault=160
upperHRedDefault=180
# define color ranges in HSV
lower_red = np.array([lowerHRedDefault*-1, minSRed, minVRed])
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

# create trackbars 
cv2.createTrackbar('Hue_Upper', 'green', upper_green[0], abs(maxHGreen-minHGreen), adjust)
cv2.createTrackbar('Hue_Lower', 'green', lower_green[0], abs(maxHGreen-minHGreen), adjust)
cv2.createTrackbar('Sat_Upper', 'green', upper_green[1], abs(maxSGreen-minSGreen), adjust)
cv2.createTrackbar('Sat_Lower', 'green', lower_green[1], abs(maxSGreen-minSGreen), adjust)
cv2.createTrackbar('Val_Upper', 'green', upper_green[2], abs(maxVGreen-minVGreen), adjust)
cv2.createTrackbar('Val_Lower', 'green', lower_green[2], abs(maxVGreen-minVGreen), adjust)
'''

cv2.namedWindow('testing')
minHTesting=0
maxHTesting=255
minSTesting=0
maxSTesting=255
minVTesting=0
maxVTesting=255
#default values
lowerHTestingDefault=0
upperHTestingDefault=255
# define color ranges in HSV

lower_testing = np.array([lowerHTestingDefault, minSTesting, minVTesting])
upper_testing = np.array([upperHTestingDefault, maxSTesting, maxVTesting]) 


# create trackbars 
cv2.createTrackbar('Hue_Upper', 'testing', upper_testing[0], abs(maxHTesting-minHTesting), adjust)
cv2.createTrackbar('Hue_Lower', 'testing', lower_testing[0], abs(maxHTesting-minHTesting), adjust)
cv2.createTrackbar('Sat_Upper', 'testing', upper_testing[1], abs(maxSTesting-minSTesting), adjust)
cv2.createTrackbar('Sat_Lower', 'testing', lower_testing[1], abs(maxSTesting-minSTesting), adjust)
cv2.createTrackbar('Val_Upper', 'testing', upper_testing[2], abs(maxVTesting-minVTesting), adjust)
cv2.createTrackbar('Val_Lower', 'testing', lower_testing[2], abs(maxVTesting-minVTesting), adjust)


#minHGreen=50 
#cv2.createTrackbar('lower_green_adjust', 'green', lower_green[0], 79, adjust)
#cv2.createTrackbar('upper_green_adjust', 'green', upper_green[0], 79, adjust)


# In[8]:

cap = cv2.VideoCapture(0)


while(1):
  
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the selected HSV colors
    #mask_red = cv2.inRange(hsv, lower_red, upper_red)
      
    #mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    mask_testing = cv2.inRange(hsv, lower_testing, upper_testing)

    # Bitwise-AND mask and original image
    #ratio='Red:Green '+str(cv2.countNonZero(mask_red))+":"+str(cv2.countNonZero(mask_green))
    #res = cv2.bitwise_and(frame,frame, mask= mask_red)
    
    #calculate the resulting image - this may be much slower than just dealing with the masks consider reverting
    '''
    res_red=cv2.bitwise_and(frame, frame, mask=mask_red)
    res_green=cv2.bitwise_and(frame, frame, mask=mask_green)
    '''
    
    res_testing=cv2.bitwise_and(frame, frame, mask=mask_testing)
    
    # add red:green ratio to window
    # cv2.putText(frame, ratio, (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2 )
    
    # take red:green measurments above this point    
    
    # all text additions need to be made AFTER measurements have been taken!
    # add adjustment slider values to window
    '''
    cv2.putText(res_red, "Low:"+str(lower_red), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2 )
    cv2.putText(res_red, "Up: "+str(upper_red), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)    
    
    cv2.putText(res_green, "Low:"+str(lower_green), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2 )
    cv2.putText(res_green, "Up: "+str(upper_green), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    '''
    
    cv2.putText(res_testing, "Low:"+str(lower_testing), (10,50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(res_testing, "Up: "+str(upper_testing), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    
    
    #live image      
    cv2.imshow('live',frame)
    
    '''
    cv2.imshow('red', res_red)
  
    cv2.imshow('green', res_green)
    '''
    
    cv2.imshow('testing', res_testing)

    #read and adjust values from sliders
    '''
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
    '''
    
    #wide open range for testing
    lower_testing[0]=minHTesting+cv2.getTrackbarPos('Hue_Lower', 'testing')
    upper_testing[0]=minHTesting+cv2.getTrackbarPos('Hue_Upper', 'testing')
    lower_testing[1]=minSTesting+cv2.getTrackbarPos('Sat_Lower', 'testing')
    upper_testing[1]=minSTesting+cv2.getTrackbarPos('Sat_Upper', 'testing')
    lower_testing[2]=minVTesting+cv2.getTrackbarPos('Val_Lower', 'testing')
    upper_testing[2]=minVTesting+cv2.getTrackbarPos('Val_Upper', 'testing')

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:




# In[ ]:



