
# coding: utf-8

# In[7]:

import cv2
import numpy


# In[8]:

def checkCams():
    '''enumerate the connected and readable video devices'''
    cameraList = []
    for i in range(0, 10):
        try:
            connected, _ = cv2.VideoCapture(i).read()
        except Excpetion, e:
            print 'video device', i, 'not avaialble - this is OK!'
        cv2.VideoCapture(i).release()
        if connected:
            cameraList.append(i)
    return cameraList

cams = checkCams()
print 'found camera devices at:', cams

for i in range(0, 30):
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    cv2.imshow('foo' , frame)
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:



