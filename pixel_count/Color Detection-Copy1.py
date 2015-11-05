
# coding: utf-8

# In[2]:

import cv2
import numpy as np


# In[86]:

#file='mb02.png'
file='green-yellow.jpg'


# In[87]:

img=cv2.imread(file, 1)


# In[88]:

# list possible flags
#flags=[i for i in dir(cv2) if i.startswith('COLOR_')]
#print flags


# In[89]:

imgHSV=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# In[90]:

lower_blue=np.array([110, 50, 50])
upper_blue=np.array([130,255,255])

lower_red=np.array([0, 100, 100])
upper_red=np.array([20, 255, 255])

lower_yellow=np.array([80, 100, 100])
upper_yellow=np.array([100, 255, 255])

lower_green=np.array([50, 100, 100])
upper_green=np.array([70, 255, 255])

#lower=lower_red
#upper=upper_red

#mask=cv2.inRange(imgHSV, lower, upper)
#res=cv2.bitwise_and(imgHSV, imgHSV, mask=mask)

mask_red=cv2.inRange(imgHSV, lower_red, upper_red)
mask_green=cv2.inRange(imgHSV, lower_green, upper_green)


# In[ ]:




# In[91]:

#cv2.imshow('res', res)
cv2.imshow('green', mask_green)
cv2.imshow('red', mask_red)
cv2.imshow('img', img)
cv2.imshow('imgHSV', imgHSV)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[3]:

green=np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print 'green', hsv_green

red=np.uint8([[[0,0,255]]])
hsv_red=cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
print 'red', hsv_red

blue=np.uint8([[[255,0,0]]])
hsv_blue=cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
print 'blue', hsv_blue

yellow=np.uint8([[[0,255, 255]]])
hsv_yellow=cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
print 'yellow', hsv_yellow


# In[93]:

print "red pix", cv2.countNonZero(mask_red)
print "green pix", cv2.countNonZero(mask_green)


# In[ ]:




# In[ ]:



