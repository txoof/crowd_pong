
# coding: utf-8

# # Imports

# In[8]:

import re
import cv2
import numpy as np
import copy
import time
import websocket


# # Functions

# In[9]:

def addText(img, text = ['your text here', 'and here'], xPos = 10, size = 1.25, textColor = (255, 255, 255),
            thickness = 1, lineType = 8, vertSpacing = 1):
    '''add a multi element list of strings to an image
    img - openCV image
    yPosition - distance in px from left edge
    size - openCV font size
    thickness - line thickness
    lineType - line type
    vertSpacing = integer (1 for single, 2 for double, etc.)'''
    # cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    vSpacing = int(vertSpacing * size * 20) #size = 1 is about 20 pixles tall
    font = cv2.FONT_HERSHEY_PLAIN
    yPos = vSpacing
    # this method still costs N calls to putText where N is the number of lines.
    for line in text:
        cv2.putText(img, str(line), (xPos, yPos), font, size, textColor, thickness, lineType )
        # increment the y position
        yPos += vSpacing
        
    return img
        

def ratio(countA, countB):
    '''calculate the ratio of colorA to colorB pixels and return a value between -1/1
    colorA is defined as the negative color and colorB is defined as the positive color
    method: (X-Y)/X where X is the larger number'''
    if countA==countB:
        return(0.0)
    if countA > countB:
        # give a negative number
        percent=-1*((countA-countB)/float(countA))
    if countA < countB:
        #give a positve number
        percent=1*((countB-countA)/float(countB))
    
    # set percent to 0.0 when the colors are in the range -.2 to .2
    if -.2 < percent < .2:
        percent = 0.0
    return(percent)


# # Classes

# In[10]:

class InputError(Exception):
    '''general error for bad input'''
    def __init__(self, value):
        self.value = value + '<-bad input'
    def __str__(self):
        return repr(self.value)
    
class LoopHalt(Exception):
    '''class for handling a loopHalt event (quit)'''
    pass

class elapsedTime:
    '''Measure elapsed time (time delta)
    timeLast - record a time for later comparison
    startTime - time variable was last inited'''
    def __init__(self):
        self.startTime = time.time()
        self.timeLast = time.time()
    
    def timeNow(self):
        '''return the time NOW'''
        return time.time()
    
    def setTime(self):
        '''record the current time'''
        self.timeLast = self.timeNow()
        
    def hasElapsed(self, elapsed = -1):
        '''return True if the timeNow  - timeLast > elapsed (in seconds)'''
        if self.timeNow() - self.timeLast > elapsed:
            return True
        else:
            return False


# this method doesn't win much.  It still costs N calls to cv2.putText for every line displayed.
class multiLine2List:
    '''create a list from strings'''
    def __init__(self):
        self.strList = []
    
    def clear(self):
        '''clear out list'''
        self.strList = []
    
    def addLine(self, string):
        '''add a line to the list'''
        self.strList.append(str(string))
    
    def printList(self):
        '''print the list line by line'''
        for l in self.strList:
            print l
    
    def numLines(self):
        '''return the number of elements'''
        return len(self.strList)

class KeyHandler:
    '''lookup keyboard input received as cv2.waitkey() input'''
    def __init__(self):
        '''create a keyhandler object with an empty dictionary
        keyMap - empty key lookup dictionary
        keyDEC - key press in decimal
        keyCHR - key press as a character
        methodReturn - list of values returned by called methods'''
        self.keyMap = {}
        self.keyDEC = 255 #Default (no key)
        self.keyCHR = None
        self.methodReturn = []
        
    
    def addKey(self, key, obj, method, description = 'Helpful description'):
        '''add an ASCII key refference and a tuple containing the following information:
        key <single chr>: 
            (object <object>[1], method <str>[2], help/description <str>[3])'''
        try:
            # check for single ASCII charactes, raise exception for anyting more
            if re.match('^[\x00-\x7F]{1}$', key) is not None:
                self.keyMap[key] = (obj, method, description)
            else:
                raise InputError(key)                
        except Exception, e:
            print 'Only single ASCII characters can be added to the dictionary:',e 
    
    def displayHelp(self):
        '''dispaly keys and desciption'''
        # consider displaying in alphabetical order
        # http://stackoverflow.com/questions/364519/in-python-how-to-i-iterate-over-a-dictionary-in-sorted-order
        print '='*20
        for key, (_, _, description) in self.keyMap.items():
            print key, '=', description
        print '\n'
        return (-3, '')

    
    def handleKey(self, key):
        '''receive input from cv2.waitkey() and run the appropriate method'''
        self.keyDEC = key & 0xFF
        self.keyCHR = chr(self.keyDEC)
        if self.keyCHR in self.keyMap:
            obj, method, description = self.keyMap[self.keyCHR]
            self.methodReturn = getattr(obj, method)()
        else:
            # set to empty if no key or an unknown key was pressed
            self.methodReturn = []
        # set to empty if None was returned    
        if self.methodReturn is None:
                self.methodReturn = []

            
class RunTime:
    '''maintain runtime state'''

    def __init__(self):
        self.displayOn = True
        pass

    def pause(self):
        '''signal pause condition'''
        self.displayOn = False
        return (-3, 'pause display')
        
    
    def unpause(self):
        '''signal unpause condition'''
        self.displayOn = True
        return (-3, 'unpause display')
    
    def quit(_):
        '''raise LoopHalt class to signal break condition'''
        raise LoopHalt
        return (-99, 'quit')
    
    def pauseGame(_):
        return(2, 'Pause game')
    
    def restart(_):
        return(3, 'Restart game')
    
    def doOver(_):
        return(4, 'Do over')
    
    def calibration(_):
        return(5, 'Calibration')
    
    def credits(_):
        return(6, 'Return to credits')
        
class ColorHSV:
    #class attributes
    
    # preset color ranges
    defaultRanges = [[0, 179, 'full'], [0, 35, 'red'], [25, 65, 'yellow'], [55, 95, 'green'], 
                     [85, 125, 'blue'], [115, 155, 'indigo'], [145, 179, 'violet']]
    
    # maximum and minimum values for Hue, Sat, Val
    hueRange = [0, 179]
    satRange = [0, 255]
    valRange = [0, 255]
    
    # track bar attributes
    sliderHue = ['Hue-', 'Hue+']
    sliderSat = ['S-', 'S+']
    sliderVal = ['V-', 'V+']
    sliderColRange = ['ColorRange']
    
    def __init__(self, name = 'default', colorRange = 0):
        self.name = name
        self.controlWinName = self.name + '_controls'
        self.text = multiLine2List()
        self.colorRange = False
        # loop counter
        iC = 0
        for i in self.defaultRanges:
            # create a regexp for finding the human readable color range in the name
            regexp = self.defaultRanges[iC][2] + '.*'
            # search the color name against the names in defaultRanges
            m = re.search(regexp, self.name, re.IGNORECASE)
            
            # if a match has been made
            if m is not None:
                # set the color range equal to the loop counter
                self.colorRange=iC
                #stop looking here
                break
            
            #increment the counter
            iC += 1
        # if a range name was not found, set the range to 0: full
        if not self.colorRange:
            self.colorRange = colorRange
        # set lower and upper values to those specified by colorRange
        self.setRangeDefault()
        
    
    def setRangeDefault(self):
        '''set hue +/- to predefined range'''
        self.lower = self.setHSVvalues( [ self.defaultRanges[self.colorRange][0],
                                        self.satRange[0], self.valRange[0]] )
        self.upper = self.setHSVvalues( [self.defaultRanges[self.colorRange][1], 
                                        self.satRange[1], self.valRange[1]] )

    
    def setHSVvalues(_, hsv = np.array( [0, 0, 0] ) ):
        '''create an numpy.array from list of values'''
        return np.array(hsv)
    
    def createTrackBars(self):
        '''create openCV HighGUI trackbars in a named window'''
        # create a named window to attach everything to
        cv2.namedWindow(self.controlWinName)
        
        # Hue Sliders
        cv2.createTrackbar(self.sliderHue[0], self.controlWinName,
                          self.lower[0], self.hueRange[1], self.adjust)
        cv2.createTrackbar(self.sliderHue[1], self.controlWinName,
                          self.upper[0], self.hueRange[1], self.adjust)
        
        # saturation sliders
        cv2.createTrackbar(self.sliderSat[0], self.controlWinName, 
                          self.lower[1], self.satRange[1], self.adjust)
        #cv2.createTrackbar(self.sliderSat[1], self.controlWinName, 
        #                 self.upper[1], self.satRange[1], adjust)
        
        # value sliders
        cv2.createTrackbar(self.sliderVal[0], self.controlWinName, 
                          self.lower[2], self.valRange[1], self.adjust)
        cv2.createTrackbar(self.sliderVal[1], self.controlWinName,
                          self.upper[2], self.valRange[1], self.adjust)
        
        cv2.createTrackbar(self.sliderColRange[0], self.controlWinName,
                          self.colorRange, len(self.defaultRanges)-1, self.adjust)
        
        # add a color swatch to the control window
        self.updateControlWindow()
        
        
    
    def syncTrackBars(self):
        '''read changes in HSV trackbar sliders'''
        
        # make a copy for comparison later
        oldHSV = copy.deepcopy(self)
        #hue
        self.lower[0] = cv2.getTrackbarPos(self.sliderHue[0], self.controlWinName)

        self.upper[0] = cv2.getTrackbarPos(self.sliderHue[1],self.controlWinName)

        #saturation
        self.lower[1] = cv2.getTrackbarPos(self.sliderSat[0], self.controlWinName)
        # currently unused
        #self.upper[1] = cv2.getTrackbarPos(self.sliderSatat[1], self.controlWinName)

        #value
        self.lower[2] = cv2.getTrackbarPos(self.sliderVal[0], self.controlWinName)
        self.upper[2] = cv2.getTrackbarPos(self.sliderVal[1], self.controlWinName)

        #color range
        self.colorRange = cv2.getTrackbarPos(self.sliderColRange[0], self.controlWinName)

        # if the color range setting has changed, update the sliders
        if self.colorRange != oldHSV.colorRange:
            # use the new color range setting to update the hue values
            self.setRangeDefault()
            cv2.setTrackbarPos(self.sliderHue[0], self.controlWinName, self.defaultRanges[self.colorRange][0])
            cv2.setTrackbarPos(self.sliderHue[1], self.controlWinName, self.defaultRanges[self.colorRange][1])
            
            #cv2.setTrackbarPos(color.sliderHue[0], color.controlWinName, color.defaultRanges[color.colorRange][0])
            #cv2.setTrackbarPos(color.sliderHue[1], color.controlWinName, color.defaultRanges[color.colorRange][1])
            self.updateControlWindow()
                
        # look for changes in the Hue sliders and update the color pallet as needed
        if (self.lower[0] != oldHSV.lower[0]) or (self.upper[0] != oldHSV.upper[0]):
        #    # update the color swatches on the control panels 
        #    self.update()        
            self.updateControlWindow()

    
    def updateControlWindow(self):
        '''update color swatch with appropriate color and text'''
        img = self.colorSwatch(color = self.midBGRcolor)
        
        # create a list of text to display
        if self.midBGRcolor() == (0, 0, 0):
            self.text.clear()
            self.text.addLine('OUT OF RANGE! Hue + < Hue -')
        else:
            self.text.clear()
            self.text.addLine('Aproximate mid color in hue range')
            self.text.addLine('Color range: ' + self.defaultRanges[self.colorRange][2])
            self.text.addLine(self.name)
        # add the text to the img
        img = addText(img, self.text.strList)
        
        # update image
        cv2.imshow(self.controlWinName, img)
    
    def colorSwatch(self, color = (255, 0, 255), xDim = 700, yDim = 100):
        img = np.zeros((yDim, xDim, 3), np.uint8)
        cv2.rectangle(img, (0, 0), (xDim, yDim), self.midBGRcolor(), -1)
        return img
        
    
    def midBGRcolor(self):
        '''calculate the aproximate middle color of a hue range'''
        colorDif=(self.upper[0] - self.lower[0])
        # negative values don't make sense, set them to 0
        if colorDif < 0:
            midHSVcolor = np.uint8([[[0, 0, 0]]])
        else:    
            midHSVcolor = np.uint8([[[self.lower[0] + (colorDif)//2, 255, 255]]])
        midBGRcolor = cv2.cvtColor(midHSVcolor, cv2.COLOR_HSV2BGR)
        return int(midBGRcolor[0][0][0]), int(midBGRcolor[0][0][1]), int(midBGRcolor[0][0][2])

    @staticmethod
    def adjust(self):
        '''dummy function used by openCV trackbars'''
        pass
    
class cvFrame:
    '''OpenCV frame object'''
    
    def __init__(self, videoDev = 0, frameWidth = 500, name = 'Live'):
        '''name - human readable name
        cap - video capture object
        frame - single frame from video stream
        frameWidth - width of sampled frame in pixles 
        mask - dictionary key: numpy.array image
        nonZero - dictionary key: sum of non-zero pixels
        result - dictionary key: bitwise and of mask and frame
        videoDev - current video device
        connectedCams - list of connected and readable cameras
        cameraPointer = pointer to currently active camera'''
        self.name = name
        self.frameWidth = frameWidth
        self.cap = cv2.VideoCapture(videoDev)
        self.hsvFrame = None
        self.frame = self.readFrame()
        self.mask = {}
        self.nonZero = {}
        self.result = {}
        self.videoDev = videoDev
        self.connectedCams = self.checkCams()
        self.cameraPointer = 0
        
    
    def checkCams(self):
        '''enumerate the connected and readable video devices'''
        cameraList = []
        for i in range(0, 10):
            connected, _ = cv2.VideoCapture(i).read()
            cv2.VideoCapture(i).release()
            if connected:
                cameraList.append(i)
        return cameraList
    
    
    def changeVideo(self):
        '''cycle through available video devices'''
        numCameras = len(self.connectedCams)
        self.cameraPointer += 1
        if self.cameraPointer > numCameras -1:
            self.cameraPointer = 0
        self.videoDev = self.connectedCams[self.cameraPointer]
        self.cap = cv2.VideoCapture(self.videoDev)
        return (-3, 'changed video device to ' + str(self.videoDev))
    
    def increaseFrameSize(self):
        '''increase sampled frame size'''
        if self.frameWidth <= 1550:
            self.frameWidth += 50
        else:
            pass
        return (-3, 'indreased frame size')
    
    def decreaseFrameSize(self):
        '''decrease sampled frame size'''
        if self.frameWidth >= 100:
            self.frameWidth += -50
        else:
            pass
        return (-3, 'decreased frame size')
    
    def resetFrameSize(self):
        '''reset framesize to default'''
        self.frameWidth = 500
        return (-3, 'reset frame size')
    
    def readFrame(self):
        '''update captured frame capture device'''
        width = self.frameWidth
        try:
            _, tempFrame = self.cap.read()
        except Exception, e:
            print 'error reading frame:', e
            
        try:
            r = float(width) / tempFrame.shape[1]
        except Exception, e:
            print 'bad frame.shape data', e
            r = 1.0
        
        dim = (int(width), int(tempFrame.shape[0] * r))
        resizedFrame = cv2.resize(tempFrame, dim, interpolation = cv2.INTER_AREA)
            
        self.frame = resizedFrame
        # convert to HSV space immediately 
        self.cvtHSV()
        return self.frame
    
    def cvtHSV(self):
        '''convert BGR frame to HSV space'''
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        return self.hsvFrame
    
    def release(self):
        '''release any active cameras'''
        for i in self.connectedCams:
            cv2.VideoCapture(i).release
        #self.cap.release()
    
    def calcMask(self, name = 'defaultName', lower = np.array( [0, 0, 0] ), 
                 upper = np.array( [179, 255, 255] )): 
        '''calculates mask based on two np.array objects with HSV values
        mask - dictionary key(name): numpy.array
                zero and non-zero pixels that represent masked pixels outside the defined range
        nonZero - dictionary key(name): numpy.array
                integer sum of non-zero pixels (unmased region)'''
        self.mask[name] = cv2.inRange(self.hsvFrame, lower, upper)
        self.nonZero[name] = cv2.countNonZero(self.mask[name])
        
    
    def calcResult(self, name = 'defaultName'):
        '''calculate a resultant image based on bitwise anding of frame and mask
        result - dictonary key(name): resultant mask frame'''
        self.result[name] = cv2.bitwise_and(self.frame, self.frame, mask = self.mask[name])


    
class WebSocket:
    '''create a web socket connection object'''
    
    
    def __init__(self, url):
        '''url - complete url in the form of \"ws://host:port/path\"
        socket - websocket object
        isConnected - boolean
        connectionTime - elapsed time object'''
        self.url = url
        self.isConnected = False
        self.socket = None
        self.connectionTime = elapsedTime()

    def connect(self):
        '''connect to a websocket server and record the attempted time'''
        self.connectionTime.setTime()
        
        #attempt to connect
        try:
            self.socket = websocket.create_connection(self.url)
            if self.socket.connected:
                self.isConnected = True
        except Exception, e:
            print 'websocket connection error:', e
            self.isConnected = False
    
    def reconnect(self, rate = 3):
        '''attempt to reconnect no more than every <rate> seconds'''
        if self.isConnected:
            pass
        else:
            if self.connectionTime.hasElapsed(rate):
                self.connect()
            else:
                pass
    
    def disconnect(self):
        '''disconnect form websocket server'''

        try:
            self.socket.close(status = 0, reason = 'done')
        except Exception, e:
            print 'error disconnecting from websocket:', e
        if not self.socket.connected:
            self.isConnected = False
        else:
            self.isConnected = True
            print 'failed to disconnect from websocket'
                
    def sendStr(self, msg):
        '''send msg as a string to the websocket'''
        try:
            self.socket.send(str(msg))
        except Exception, e:
            print 'error sending to socket:', e
            print ' is the websocket server running at', self.url + '?'
            self.isConnected = False       

            
class MsgHandler:
    '''display messages in open CVframe'''
    def __init__(self):
        '''msgList - dictionary of all messages to be displayed
        msgTime - record of last message update time'''
        self.msgList = {}
        self.msgTime = elapsedTime()
        
    def addMsg(self, msgID, msg, serialize = True):
        '''add a message to the queue to display
        msgID - (str) uniqe identifyer for message
        msg - (str) message to be displayed
        seralize - (bool) add a unique serial number so messages of the same type are not overwritten'''
        # sanitize everything into strings
        msgID = str(msgID)
        msg = str(msg)
        
        self.msgTime.setTime() # record the time last time messages were updated
        if serialize:
            self.msgList[msgID + '.' + str(self.msgTime.timeNow())] = msg
        else:
            self.msgList[msgID] = msg
        
    def delMsg(self, msgID):
        '''delete a message using the message id'''
        if msgID in self.msgList:
            del self.msgList[msgID]
        else:
            pass
    
    def delAllMsg(self, msgType):
        '''delete all messages of msgType'''
        for key in self.msgList.keys():
            regexp = msgType+'.*'
            match = re.search(regexp, key)
            if match is not None:
                self.delMsg(key)


# ## Classes In Training

# In[15]:

class Throttle:
    '''dictionary of timmer objects'''
    def __init__(self):
        self.timers = {}
    
    def add(self, timer, rate = 0):
        '''add a timer object
        timer - name of timer
        rate - frequency'''
        self.timers[timer] = [elapsedTime(), rate]
        return True
    
    def delete(self, timer):
        '''delete a timer object
        timer - name of timer to remove'''
        try:
            del self.timers[timer]
        except Exception, e:
            print 'problem deleting timer; probable key error:', e
        return True
    
    def adjustRate(self, timer, adjust):
        '''adjust timer rate
        adjust - amount to adjust by'''
        if not (isinstance(adjust, float) or isinstance(adjust, int)):
            print 'type error (must be int or float):', adjust
            return False
        try:
            self.timers[timer][1] += adjust
        except Exception, e:
            print 'problem adjusting; probable key error:', e
        return True
    
    def check(self, timer):
        '''check state of throttle entity and update if necessary'''
        if timer in self.timers.keys():
            myTimer = self.timers[timer][0]
            myRate = self.timers[timer][1]
            if myTimer.hasElapsed(myRate):
                myTimer.setTime()
                return True
            else:
                return False
        else:
            print 'unknown timer:', timer
            return False
    
    
    


# # testing
# myThrottle = Throttle()
# myThrottle.add('trackBar', .5)
# myThrottle.add('maskCalc', .05)
# myThrottle.add('capture', .05)
# myThrottle.add('socket', 0)
# myThrottle.add('display', .1)
# 
# myThrottle.check('mask')

# # Init Objects & Vars

# In[18]:

def main():
    color0 = 'UP - Green' # up color
    color1 = 'DOWN - Yellow' # down color
    url = 'ws://localhost:9000/ws'

    myRunTime = RunTime()
    myKeyHandler = KeyHandler()
    userMessages = MsgHandler()
    channels = [ColorHSV(color0), ColorHSV(color1)]
    myFrame = cvFrame(0)
    myWebSocket = WebSocket(url)
    myThrottle = Throttle()
    
    # add keys, objects, methods and help strings to the key handler
    myKeyHandler.addKey('h', myKeyHandler, 'displayHelp', 'display this help screen')
    myKeyHandler.addKey('?', myKeyHandler, 'displayHelp', 'display this help screen')

    myKeyHandler.addKey('Q', myRunTime, 'quit', 'stop execution')
    myKeyHandler.addKey('p', myRunTime, 'pause', 'pause live display')
    myKeyHandler.addKey('u', myRunTime, 'unpause', 'unpause live display')
    myKeyHandler.addKey('P', myRunTime, 'pauseGame', 'pause game')
    myKeyHandler.addKey('R', myRunTime, 'restart', 'restart game')    
    myKeyHandler.addKey('O', myRunTime, 'doOver', 'restart point')
    myKeyHandler.addKey('C', myRunTime, 'calibration', 'return to calibration screen')
    myKeyHandler.addKey('D', myRunTime, 'credits', 'return to credits screen')


    myKeyHandler.addKey('-', myFrame, 'decreaseFrameSize', 'decrease frame size')
    myKeyHandler.addKey('=', myFrame, 'increaseFrameSize', 'increase frame size')
    myKeyHandler.addKey('0', myFrame, 'resetFrameSize', 'reset frame size to default (500px)')    
    myKeyHandler.addKey('V', myFrame, 'changeVideo', 'change video device to next availalbe camera')
        
    # add throttle objects
    myThrottle.add('trackBars', .5)
    myThrottle.add('maskCalc', .05)
    myThrottle.add('capture', .05)
    #myThrottle.add('socket', 0) # this has < 1% CPU impact and can delay or miss messages sent to game
    myThrottle.add('display', .05)

    # create trackbar windows
    for color in channels:
        color.createTrackBars()
     
    
    # bodge for ensuring that everything initializes properly with the throttle
    myFrame.readFrame()
    for color in channels:
        myFrame.calcMask(color.name, lower = color.lower, upper = color.upper)
        myFrame.calcResult(color.name)

    while True:
        try:
            # get key input every cycle and it's response
            myKeyHandler.handleKey(cv2.waitKey(1))
        except LoopHalt:
            break

        # read current frame
        # throttle 
        if myThrottle.check('capture'):
            myFrame.readFrame()

        # split into two sepperate for loops for independent throttling
        if myThrottle.check('trackBars'):
            # update trackbars
            for color in channels:
                color.syncTrackBars()

        # throttle mask calculation and ratio calculation
        if myThrottle.check('maskCalc'):
            # calculate mask and resultant frames
            for color in channels:  
                myFrame.calcMask(color.name, lower = color.lower, upper = color.upper)
                # only calculate resultant frames if the display is on
                if myRunTime.displayOn:
                    myFrame.calcResult(color.name)
            # moved into throttle check
            # calculate ratio of pixels in each channel 
            colorRatio = ratio(myFrame.nonZero[color0], myFrame.nonZero[color1])
            userMessages.addMsg('ratio', 'ratio: ' + str(colorRatio), False)        

        # add message text to the frame
        msgList = []
        for key in userMessages.msgList:
            msgList.append(userMessages.msgList[key])
        addText(myFrame.frame, msgList)

        # check web socket state
        if myWebSocket.isConnected:
            # send command messages to the web socket
            if len(myKeyHandler.methodReturn) > 0 and myKeyHandler.methodReturn[0] > 0:
                myWebSocket.sendStr(myKeyHandler.methodReturn[0])
            # send color ratio to web socket
            myWebSocket.sendStr(colorRatio)
            # remove websocket errors
            userMessages.delMsg('error.websocket')
        else:
            myWebSocket.reconnect(3)
            # add an error message to the list and unpause the display
            userMessages.addMsg('error.websocket', 'socket server disconnected', False)
            myRunTime.displayOn = True
                
        # display runtime commands on terminal
        if len(myKeyHandler.methodReturn) > 0:
            print myKeyHandler.methodReturn


        ####FIXME bodge for adding upper and lower text to each frame
        channelInfo ={}
        # get the color channel names and values and store in dictionary
        for color in channels:
            channelInfo[color.name] = (color.lower, color.upper)

        # throttle display output
        if myThrottle.check('display'):
            # update live and resultant windows
            if myRunTime.displayOn:
                #live window
                cv2.imshow(myFrame.name, myFrame.frame)

                for key in myFrame.result:
                    # bodge for adding text for testing
                    resultText = []
                    resultText.append('NonZero Px: ' + str(myFrame.nonZero[key]) )
                    resultText.append('L: ' + str(channelInfo[key][0]))
                    resultText.append('U: ' + str(channelInfo[key][1]))
                    #addText(myFrame.result[key], ['NonZero Px: ' + str(myFrame.nonZero[key]) ])
                    addText(myFrame.result[key], resultText)
                # this is a bit kludgy, but it is the simplest way to join two frames together
                cv2.imshow('Up & Down', np.concatenate((myFrame.result[color0], myFrame.result[color1]), axis = 1))

    # clean up 
    # release video devices
    myFrame.release()
    # clean up windows
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    # close websocket
    myWebSocket.disconnect()


# In[ ]:




# In[ ]:




# In[ ]:

main()


# In[ ]:

#myFrame.cap.release()


# In[ ]:

#%prun main()


# In[ ]:

#myFrame.release()
#cv2.destroyAllWindows()
#cv2.waitKey(1)

