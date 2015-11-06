
# coding: utf-8

# In[1]:

import cv2
import numpy as np


# In[9]:

red=np.uint8([[[0,0,255]]])
hsv_redLow=cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
print 'HSV red - Low', hsv_redLow

yellow=np.uint8([[[0,255, 255]]])
hsv_yellow=cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
print 'HSV yellow', hsv_yellow

green=np.uint8([[[0,255,0]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print 'HSV green', hsv_green

ltblue=np.uint8([[[255,255,0]]])
hsv_ltblue=cv2.cvtColor(ltblue, cv2.COLOR_BGR2HSV)
print 'HSV ltblue', hsv_ltblue

dkblue=np.uint8([[[255, 0, 0]]])
hsv_dkblue=cv2.cvtColor(dkblue, cv2.COLOR_BGR2HSV)
print 'HSV dkblue', hsv_dkblue

indigo=np.uint8([[[255, 255, 255]]])
hsv_indigo=cv2.cvtColor(indigo, cv2.COLOR_BGR2HSV)
print 'HSV indigo', hsv_indigo


# In[ ]:




# In[ ]:



