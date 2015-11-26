
# coding: utf-8

# In[2]:

import cv2


# In[5]:

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

