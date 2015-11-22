
# coding: utf-8

# # Imports

# In[ ]:

import cv2
import numpy as np
import re
import copy
from websocket import create_connection
import websocket
import time


# # Classes

# In[ ]:

## Classes
class outputValue:
    '''Recording the float output value from the video sampling'''
    def __init__(self):
        self.value = 0.0


        
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
        #self.timeLast = time.time()
        self.timeLast = self.timeNow()
        
    def hasElapsed(self, elapsed = -1):
        '''return True if the timeNow  - timeLast > elapsed (in seconds)'''
        if self.timeNow() - self.timeLast > elapsed:
            return True
        else:
            return False

class loopHalt(Exception): 
    '''class for handling a loopHalt event (quit)'''
    pass

class colorHSV:
    '''Form a range of values for HSV colorspace filtering based on color:
    
    name -- a user readable name that includes one of the color ranges 
            such as: 'Color One - red'
    colorRange -- select from a predefined color range (default is 0)
    
        pre defined color ranges in terms of Hue (0-179)
        
        Range Number - human name - Hue Range
        0            - full       - 0-179
        1            - red        - 0-35
        2            - yellow     - 25-65
        3            - green      - 55-95
        4            - blue       - 85-125
        5            - indigo     - 115-155
        6            - violet     - 145-179
    '''
    # class attributes
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

    #sliderHue = ['Hue-', 'Hue+']
    #sliderSat = ['S-', 'S+']
    #sliderVal = ['V-', 'V+']
    #sliderColRange = ['CR']
    
    
    
    def __init__(self, name='default', colorRange=0):
        '''Init an HSV Color Range object consiting of a 3 element numpy.array
            lower -- lower end of color space range for filtering
            upper -- upper end of color space range for filtering
            colorRange -- one of the predefined color ranges; -1 by default
            controlWinName - name for reffering to an openCV HighGUI window
        '''
        #Attributes
        self.name = name

        # set the name for a control slider window
        self.controlWinName = self.name + '_controls'
         
        # integer loop counter
        iC=0
        
        # temporarily set self.colorRange to false
        self.colorRange = False
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
            
        # set to default color range
        self.setRangeDefault()
        #self.copy = self.deepCopy()
    
    def setRangeDefault(self):
        '''use the predefined defaults to set hue range'''
        # set the lower and upper ranges based on values from the default ranges
        self.lower = self.setHSVvalues( [ self.defaultRanges[self.colorRange][0],
                                        self.satRange[0], self.valRange[0]] )
        self.upper = self.setHSVvalues( [self.defaultRanges[self.colorRange][1], 
                                        self.satRange[1], self.valRange[1]] )
    
    def setHSVvalues(self, hsv = np.array( [0, 0, 0] )):
        '''sets a list of values as type numpy.array()'''
        return np.array(hsv)
    
    
    def createTrackBars(self):
        '''Create openCV HighGUI trackbars in a window that matches name + _contorls'''
        
        # create a named window to attach everything to
        cv2.namedWindow(self.controlWinName)
        
        # Hue Sliders
        cv2.createTrackbar(self.sliderHue[0], self.controlWinName,
                          self.lower[0], self.hueRange[1], adjust)
        cv2.createTrackbar(self.sliderHue[1], self.controlWinName,
                          self.upper[0], self.hueRange[1], adjust)
        
        # saturation sliders
        cv2.createTrackbar(self.sliderSat[0], self.controlWinName, 
                          self.lower[1], self.satRange[1], adjust)
        #cv2.createTrackbar(self.sliderSat[1], self.controlWinName, 
        #                 self.upper[1], self.satRange[1], adjust)
        
        # value sliders
        cv2.createTrackbar(self.sliderVal[0], self.controlWinName, 
                          self.lower[2], self.valRange[1], adjust)
        cv2.createTrackbar(self.sliderVal[1], self.controlWinName,
                          self.upper[2], self.valRange[1], adjust)
        
        cv2.createTrackbar(self.sliderColRange[0], self.controlWinName,
                          self.colorRange, len(self.defaultRanges)-1, adjust)
        
    def syncTrackBars(self):
        '''record the position of openCV trackbars in lower and upper'''
        
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
            cv2.setTrackbarPos(color.sliderHue[0], color.controlWinName, color.defaultRanges[color.colorRange][0])
            cv2.setTrackbarPos(color.sliderHue[1], color.controlWinName, color.defaultRanges[color.colorRange][1])            
                
        # look for changes in the Hue sliders and update the color pallet as needed
        if (self.lower[0] != oldHSV.lower[0]) or (self.upper[0] != oldHSV.upper[0]):
            # update the color swatches on the control panels 
            self.update()        

    def update(self):
        '''update windows and trackbars as needed'''
        # update the control windows with a new color swatch
        updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                    colorRange=color.defaultRanges[color.colorRange][2])
         
    def midBGRcolor(self):
        '''return the middle value between the upper and lower hue values in BGR space'''
        colorDelta=(self.upper[0] - self.lower[0])
        # negative values don't make sense, set them to 0
        if colorDelta < 0:
            midHSVcolor = np.uint8([[[0, 0, 0]]])
        else:    
            midHSVcolor = np.uint8([[[self.lower[0] + (colorDelta)//2, 255, 255]]])
        midBGRcolor = cv2.cvtColor(midHSVcolor, cv2.COLOR_HSV2BGR)
        return int(midBGRcolor[0][0][0]), int(midBGRcolor[0][0][1]), int(midBGRcolor[0][0][2])
"""
class cvFrame:
    
    def __init__(self, videoDev = 0, frameWidth = 500):
        '''create a frame object that holds all of the frame, hsv frame and mask data for a filter
        videoDev - numeration for video capture device; 0 is default
        frameWidth - width in px of video capture; 500 is default
        frame - cv2.VideoCapture(<video device>)
        name - human readable name for refference 
        hsvFrame - frame converted into HSV space
        mask - a mask calculated based on properties passed
        result - the result of a bitwise_and of the frame and the mask 
        '''
        self.cap = cv2.VideoCapture(videoDev)
        #_, self.frame = self.cap.read()
        self.frame = self.readFrame()
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.mask = self.calcMask()
        self.result = self.calcRes()
    
    # ideally this should update the HSV frame as well.  Don't know how to make that happen
    def readFrame(self, width = 500):
        '''update the stored frame from the video capture device'''
        #_, self.frame = self.cap.read() 
        try:
            _, tempFrame= self.cap.read()
        except Exception, e:
            print 'error reading frame:', e
        
        # look for bad data in the frame; if there's bad data simply set r =1 
        # this is an ugly hack, but should allow things to continue running
        try:
            r = float(width) / tempFrame.shape[1]
        except Exception, e:
            print 'bad tempFrame.shape data:', e
            r = 1.0
        dim = (int(width), int(tempFrame.shape[0] * r))
        resizedFrame = cv2.resize(tempFrame, dim, interpolation = cv2.INTER_AREA)
        self.frame = resizedFrame
        return self.frame
        
    def cvtHSV(self):
        '''create an HSV version of the frame'''
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        return self.hsvFrame
        
    def release(self):
        '''release the video capture device'''
        self.cap.release()
    
    def calcMask(self, lower = np.array( [0, 0, 0] ), upper = np.array( [179, 255, 255] )):
        '''calculate a mask based on two np.array objects with HSV values'''
        self.mask = cv2.inRange(self.hsvFrame, lower, upper, )
        self.nonZero = cv2.countNonZero(self.mask)
        return self.mask
    
    def calcRes(self):
        self.result = cv2.bitwise_and(self.frame, self.frame, mask = self.mask)
        return self.result
"""
        
class webSocket:
    #### Fixme - add a disconnect method
    '''create a web socket connection
    url - complete url in the form of ws://host:<port>/path
    socket - websocket object
    isConnected - boolean
    connectedAt - time the connection was made
    attemptedAt - time a connection attempt was made'''
    def __init__(self, url):
        self.url = url
        self.isConnected = False
        self.socket = None
        self.connectionTime = elapsedTime()
        #self.socket = self.connect
        # still working out how to use the elapsed time class
    
    ####FIXME! totally busted
    def connect(self):
        '''connect to the web socket'''
        # set the time that the connection was attempted
        self.connectionTime.setTime()
        
        # attempt to connect
        try:
            self.socket = websocket.create_connection(self.url) 
            if self.socket.connected:
                self.isConnected = True
        except Exception, e:
            self.isConnected = False
    
    def reconnect(self, rate = 3):
        '''attempt to reconnect no more than every <rate> seconds'''
        if self.isConnected:
            pass
        else:
            # check to see if enough time has elapsed before attempting a connection
            if self.connectionTime.hasElapsed(rate):
                self.connect()
            else:
                pass
    
    def disconnect(self):
        '''not yet implemented'''
        print 'disconnect does NOTHING'
        pass
    
    def send(self, msg):
        try:
            self.socket.send(msg)
        except Exception, e:
            print 'error sending to socket:', e
            print 'is the web socket server running?'
            self.isConnected = False

class msgHandler:
    '''important messages to display on the live window'''
    def __init__(self):
        self.msgList = {}
        self.msgTime = elapsedTime()
        
    def addMsg(self, msgID, msg):
        '''add messages to the list
        msgID - unique identifyer for message
        msg - message to be displayed'''
        self.msgTime.setTime()
        self.msgList[msgID+ '.' +str(self.msgTime.timeNow())] = msg
    
    def delMsg(self, msgID):
        '''remove messages to the list
        msgID - unique identifyer for message'''
        if msgID in self.msgList:
            del self.msgList[msgID]
        else:
            pass
        
    def delAllMsg(self, msgType):
        for key in self.msgList.keys():
            regexp = msgType+'.*'
            match = re.search(regexp, key)
            if match is not None:
                self.delMsg(key)     
    
####FIXME - change the name to keyHandler   
class keyHandlerN:
    '''handle key presses from openCV waitkey()
    keyPressDEC - Decimal equivalent of value
    keyPressCHR - ASCII character value
    functionCall - function to execute based on keypress
    sendCommand - command to send to websocket server'''
    def __init__(self):
        self.keyPress = None
        self.keyPressDEC = 255
        self.keyPressCHR = None
        self.functionCall = doNothing()
        self.sendCommand = None
        self.displayMsg = ''
        self.msgType = '' 
        
    def keyInput(self, keypress):
        self.keyPress = keypress
        self.keyPressDEC = self.keyPress & 0xFF
        self.keyPressCHR = chr(self.keyPressDEC)

####FIXME remove this class it has been replaced by keyHandlerN
class keyHandler:
    '''handle key presses'''
    helpDict = {
        'C': 'Restart calibration',
        'h': 'Print help text to screen',
        'P': 'Restart point (do over)',
        'p': 'Pause live display',
        'Q': 'Quit',
        'R': 'Restart game',
        'u': 'Unpause live display',
        'Z': 'Return to credit screen'        
    }
    
    def __init__(self):
        '''keyPress - OpenCV waitKey() value
        keyPressDEC - Decimal equivalent of value
        keyPressCHR - ASCII character value
        functionCall - function to execute based on keypress
        sendCommand - command to send to websocket server
        functionMap - map keypresses to functions
        displayMsg - text to display in live window
        msgType - type of message: info, 
        
        '''
        self.keyPress = None
        self.keyPressDEC = 255
        self.keyPressCHR = None
        self.functionCall = doNothing()
        self.sendCommand = None
        self.displayMsg = ''
        self.msgType = ''
        self.functionMap = {
            'C': self.calibration,
            'h': self.printHelp,
            'P': self.restartPoint,
            'p': self.pauseDisplay,
            'Q': self.quit,
            'R': self.restartGame,
            'u': self.unpauseDisplay,
            'Z': self.credits,
        }
        
    
    def keyInput(self, keyPress):       
        self.keyPress = keyPress
        self.keyPressDEC = self.keyPress & 0xFF
        self.keyPressCHR = chr(self.keyPressDEC)
       
        if self.keyPressCHR in self.functionMap:
            self.functionMap[self.keyPressCHR]()
    
        #elif self.keyPressDEC == 255:
        # if the key is not in the function map reset
        else:
            # reset the send command to none 
            self.sendCommand = None
            # reset the display text to ''
            self.displayMsg = ''
            self.msgType = ''    

    def printHelp(self):
        #for key in self.helpDict:
        #    print key, self.helpDict[key]
        self.returnCmd(-4, 'info')
    
    def quit(self):
        self.functionCall = doNothing()
        raise loopHalt
        
    def restartGame(self):
        self.returnCmd(3, 'info')

    def restartPoint(self):
        self.returnCmd(4, 'info')
   
    def calibration(self):
        self.returnCmd(5, 'info')
        
    def credits(self):
        self.returnCmd(6, 'info')
        
    def pauseDisplay(self):
        self.returnCmd(-2, 'state')
    
    def unpauseDisplay(self):
        self.returnCmd(-3, 'state')
    
    def returnCmd(self, command, msgType = 'None'):
        self.sendCommand = command
        if self.keyPressCHR in self.helpDict:
            helpDict = self.helpDict[self.keyPressCHR]
        else:
            helpDict = 'Undocumented feature'
        self.displayMsg = helpDict + ': Code ' + str(self.sendCommand)
        self.msgType = msgType

class runTimeState:
    ### Consider merging in the runTime variable as runningTime
    '''container for runtime variables and key handler
    pause - pause state (bool)
    displayOff - display state (bool)
    command - numerical command to send to socket server 
    displayMsg - user readable message corresponding to command
    keyHandler - keyhandler object for reading key presses
    '''
    helpDict = {
        'C': 'Restart calibration',
        'h': 'Print help text to screen',
        'P': 'Restart point (do over)',
        'p': 'Pause live display',
        'Q': 'Quit',
        'R': 'Restart game',
        'u': 'Unpause live display',
        'Z': 'Return to credit screen'        
        }

    def __init__(self):
        self.pause = False
        self.displayOff = False
        self.command =  ''
        self.msgType = ''
        self.displayMsg = ''
        self.keyHandler = keyHandlerN()
        self.functionMap = {
            'C': self.calibration,
            'h': self.printHelp,
            'P': self.restartPoint,
            'p': self.pauseDisplay, 
            'Q': self.quit,
            'R': self.restartGame,
            'u': self.unpauseDisplay,
            'Z': self.credits,
        }
    
    def keyInput(self, keyPress):
        self.keyHandler.keyInput(keyPress)
        if self.keyHandler.keyPressCHR in self.functionMap:
            self.functionMap[self.keyHandler.keyPressCHR]()
        # if the key is not in the function map reset
        else:
            # reset the send command to none 
            self.command = None
            # reset the display text to ''
            self.displayMsg = ''
            self.msgType = ''
            
   
    
    def printHelp(self):
        ####FIXME - add the help by magic?
        pass
    
    def restartGame(self):
        self.sendCmd(3, 'info')

    def restartPoint(self):
        self.sendCmd(4, 'info')
    
    def calibration(self):
        self.sendCmd(5, 'info')
    
    def credits(self):
        self.sendCmd(6, 'info')
    
    def pauseDisplay(self):
        self.pause = True
        self.displayOff = True
        self.sendCmd(-2, 'state')
        
    def unpauseDisplay(self):
        self.pause = False
        self.displayOff = False
        self.sendCmd(-3, 'state')

    def sendCmd(self, command ='null', msgType = 'info'):
        '''format a command to display to user and send to websocket
        command - command to send
        msgType - type of message (info, state, etc.)'''
        self.command = command
        self.msgType = msgType
        if self.keyHandler.keyPressCHR in self.helpDict:
            helpLookup = self.helpDict[self.keyHandler.keyPressCHR]
        else:
            helpLookup = 'Undocumented feature'
        self.displayMsg = helpLookup + ': Code ' + str(self.command)
    
    def quit(self):
        self.functionCall = doNothing()
        raise loopHalt
        


# # sub routines

# In[ ]:


def adjust(x):
 '''Place holder function for opencv.getTrackBar function.
 Simply passes trackbar position to a variable'''
 pass

def addText(img, text = 'your text here', position = (10, 25), 
         textColor = (0, 255, 0), size = 1.25, thickness = 1, lineType = 8):
 # cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
 '''Add text to an openCV image'''
 font = cv2.FONT_HERSHEY_PLAIN
 cv2.putText(img, text, position, font, size, textColor, thickness, lineType)
 return img

def colorSwatch(swatchColor = (255, 0, 255), xDim = 700, yDim = 100):
 img = np.zeros((yDim, xDim, 3), np.uint8)
 cv2.rectangle(img, (0, 0), (xDim, yDim), swatchColor, -1) 
 return img

# add branch to detect "out of range"
def updateControlWindow(name, midBGRcolor, colorRange='' ):
 '''update the control pannel windows with color swatches and text'''
 img = colorSwatch(swatchColor = midBGRcolor)
 if midBGRcolor == (0, 0, 0):
     img = addText(img, text = 'Hue + < Hue - OUT OF RANGE!')
 else:
     img = addText(img, textColor = (255, 255, 255), text = 'Aproximate middle color of hue range')
     img = addText(img, textColor = (255, 255, 255), text = 'Color range: ' + colorRange, position = (10, 50))
     img = addText(img, textColor = (255, 255, 255), text = name, position = (10, 75))
 cv2.imshow(name, img)
 #return img

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

def displayMessages(img, msgDict = {}):
 '''display a list of important messages by adding them to the specified img'''
 msgCounter = 0
 for i in msgDict:
     addText(img = img, text = msgDict[i], position = (10, 25+25*msgCounter))
     msgCounter += 1
 
 return img

def sendCommand(websocket, command = 'null', num = 1):
 '''send a command num times to the websocket object'''
 if websocket.isConnected:
     for i in range(num):
         ws.send(str(command))
 # FIXME WTF is this for?  I don't think we return anything here.
 return
 
def doNothing():
 '''placeholder function that does nothing'''
 ####FIXME - this can probably be fixed by using the @staticmethod decorator in the class
 pass


# # New classes 
# Classes in training

# In[ ]:

class cvFrame:
    
    def __init__(self, videoDev = 0, frameWidth = 500, name = 'Live'):
        '''create a frame object that holds all of the frame, hsv frame and mask data for a filter
        videoDev - numeration for video capture device; 0 is default
        frameWidth - width in px of video capture; 500 is default
        frame - cv2.VideoCapture(<video device>)
        name - human readable name for refference 
        hsvFrame - frame converted into HSV space
        mask - dictonary of calculated masks
        nonZero - dictionary of nonZero pixels 
        result - the result of a bitwise_and of the frame and the mask 
        joinedResultImg - concantination of all resultant frames along axis 1
        '''
        self.cap = cv2.VideoCapture(videoDev)
        #_, self.frame = self.cap.read()
        self.frame = self.readFrame()
        self.hsvFrame = self.cvtHSV()
        #self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.name = name
        self.mask = {}
        self.nonZero = {}
        self.result = {}
        self.joinedResultImg = None
        self.joinedResultName = ''
        #self.mask = self.calcMask()
        #self.result = self.calcRes()
        
    
    # ideally this should update the HSV frame as well.  Don't know how to make that happen
    def readFrame(self, width = 500):
        '''update the stored frame from the video capture device'''
        #_, self.frame = self.cap.read() 
        try:
            _, tempFrame= self.cap.read()
        except Exception, e:
            print 'error reading frame:', e
        
        # look for bad data in the frame; if there's bad data simply set r =1 
        # this is an ugly hack, but should allow things to continue running
        try:
            r = float(width) / tempFrame.shape[1]
        except Exception, e:
            print 'bad tempFrame.shape data:', e
            r = 1.0
        dim = (int(width), int(tempFrame.shape[0] * r))
        resizedFrame = cv2.resize(tempFrame, dim, interpolation = cv2.INTER_AREA)
        self.frame = resizedFrame
        
        # update the HSV space version of the frame
        self.cvtHSV()
        return self.frame
        
    def cvtHSV(self):
        '''create an HSV version of the frame'''
        self.hsvFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        return self.hsvFrame
        
    def release(self):
        '''release the video capture device'''
        self.cap.release()
    
    def calcMask(self, name = 'defaultName', lower = np.array( [0, 0, 0] ), upper = np.array( [179, 255, 255] )):
        '''calculate a mask based on two np.array objects with HSV values'''
        #self.mask = cv2.inRange(self.hsvFrame, lower, upper, )
        #self.nonZero = cv2.countNonZero(self.mask)
        self.mask[name] = cv2.inRange(self.hsvFrame, lower, upper)
        self.nonZero[name] = cv2.countNonZero(self.mask[name])
        return self.mask
    
    def calcRes(self, name = 'defaultName'):
        '''calculate a resultant image based on the mask and the live frame'''
        self.result[name] = cv2.bitwise_and(self.frame, self.frame, mask = self.mask[name])
        return self.result


# In[ ]:

### Vars that should probably live in a configuration file

####FIXME this can probably all be moved into a ConfigParser object
socketURL = 'ws://localhost:9000/ws'
color0Name = 'UP'
color1Name = 'DOWN'
videoDevice = 0 


### Init Objects
# create a connection to the web socket handler object
ws = webSocket(socketURL)
ws.connect()

# create the colorHSV objects
channels = [colorHSV(color0Name), colorHSV(color1Name)]

# keep track of runtime state and manage key presses
myRunState = runTimeState()

# object for holding user messages
usrMessages = msgHandler()

# openCV camera object
####FIXME cvFrame should try <videoDevice> then fall back to 0 if it is not found
myFrame = cvFrame(videoDevice)


##### TESTING #
#create and open cv window for testing
#img = cv2.imread('./images/Demo_Start.png')
#cv2.imshow('test', img)
# TESTING #####


# initialize track bar windows
# loop counter for placing windows
####FIXME move this into a sub somehow?
windowCount = 0
for color in channels:
    color.createTrackBars()
    # shift each window over a bit
    cv2.moveWindow(color.controlWinName, windowCount*400, 0)
    updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])
    windowCount += 1

# start loop
while True:
    
    # get key presses from cv2.waitKey() and send to the key handler in the run state
    try:
        myRunState.keyInput(cv2.waitKey(1))
    except loopHalt:
        # clean up on halt exception
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        break

    ####FIXME - I still don't love this.  There is probably a more pythonic way to do this.
    # send messages to websocket and display
    if myRunState.command is not None:
        # send a command to the web socket
        sendCommand(command = myRunState.command, websocket = ws)
        # delete old messages of the same type just created
        usrMessages.delAllMsg(myRunState.msgType)
        # add new messages
        usrMessages.addMsg(myRunState.msgType, myRunState.displayMsg)        
        
    # read and convert frame from video device
    myFrame.readFrame()
        
    # sync trackbars 
    # loop over each channel and make updates as needed
    for color in channels:
        # sync the tracbars - this will update the color slider windows and color swatches
        color.syncTrackBars()
        # calculate the mask based on the settings 
        myFrame.calcMask(lower = color.lower, upper = color.upper, name = color.name)
        # calculate resultant here? - this may be a bad idea as is not needed when paused (save some cycles)
 
    # display the resultant images if the display is not paused
    if not myRunState.displayOff:
        for color in channels:
            # if the display is not off, calculate the resultant frame and display
            myFrame.calcRes(color.name)
            # add in the pixle count 
            addText(myFrame.result[color.name], text = 'NonZero pix: ' + str(myFrame.nonZero[color.name]))
            # add in the HSV settings
            
            # display each image
            cv2.imshow(color.name, myFrame.result[color.name])
            # find a way to np.concantinate the images
        # display the live image    
        # add in messages and expire old messages
        cv2.imshow(myFrame.name, myFrame.frame)
        

    # calculate ratio
    # check web socket and write out data
    # update displays with current frame and messages
    # delete old messages of type info, state
    
myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
# FIXME disconnect gracefully from the websocket 
ws.disconnect()


# In[ ]:

help(addText)


# In[ ]:

for color in channels:
    myFrame.calcMask(lower = color.lower, upper = color.upper, name = color.name)
    
cv2.imshow('foo', myFrame.mask['DOWN'])
cv2.imshow('bar', myFrame.mask['UP'])
cv2.waitKey(1)


# In[ ]:

usrMessages.msgList
cv2.VideoCapture(0).release()


# In[ ]:




# In[ ]:

myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
# FIXME disconnect gracefully from the websocket 
ws.disconnect()


# In[ ]:


# init variables

### Configuration Variables ###

# color channels
colorA = colorHSV('UP - Green')
colorB = colorHSV('DOWN - Violet')
channels = [colorA, colorB]


# display name for output window
channelDisplayName = colorA.name + ' : ' + colorB.name
liveDisplayName = 'Live'
# live frame object
myFrame = cvFrame(0)

# video stream device
videoDev = 1

#web Socket Server
socketURL = 'ws://localhost:9000/ws'

### Variable Inititialziation ###

#dictionary for saving the pixel count
pixelCount = {}

# dictionary for saving the calculated masks
masks = {}

#set output value to class outputValue; variable be sent to web socket
output = outputValue

# default settings
pause = False
displayOff = False


##### Non User Defined Objects ####

# init the list of important display messages
usrMessages = msgHandler()

# create a connection to the web socket handler object
ws = webSocket(socketURL)
ws.connect()

# keep track of running time as an elapsedTime object
runTime = elapsedTime()
# keep track of time that a message is displayed
msgTime = elapsedTime()

# define the keyhandler object
myKeyHandler = keyHandler()

#### TESTING
myRunState = runTimeState()

### Initialize Systems ###
# init trackbars for each channel

# loop counter for placing windows
windowCount = 0
for color in channels:
    color.createTrackBars()
    # shift each window over a bit
    cv2.moveWindow(color.controlWinName, windowCount*400, 0)
    updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])
    windowCount += 1

#FIXME this is kludgy and I don't love it.  Perhaps a function/class to do this
# record all created windows in a list, then move them all logically together 
# right now they are moved as they are created (see above loop)
# experiment for moving windows around 
cv2.namedWindow(channelDisplayName)
cv2.namedWindow(liveDisplayName)
cv2.moveWindow(channelDisplayName, 0, 300)
cv2.moveWindow(liveDisplayName, 0, 350) 

    
    
# begin looping until user quits
while True:     
   
    # capture keypresses and handle them
    
    #### TESTING 
    myKeyPress = cv2.waitKey(1)
    # halt on loopHalt exception
    try:
        myKeyHandler.keyInput(myKeyPress)
        # TESTING - switch this line back
        #myKeyHandler.keyInput(cv2.waitKey(1))
        #execute the functioncall that has been set based on keyPress
        myKeyHandler.functionCall
    except loopHalt:
        # clean up on halt exception
        myFrame.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        break
    
    
    #### TESTING - trying out new keyhandler
    myRunState.keyInput(myKeyPress)
    
    
    
    # handle key presses
    
    if myKeyHandler.sendCommand is not None:
        # record the time that a keypress came in
        msgTime.setTime()
        sendCommand(command = myKeyHandler.sendCommand, websocket = ws)
        usrMessages.addMsg(myKeyHandler.msgType+str(msgTime.timeNow()), myKeyHandler.displayMsg)
        # handle special cases (pause, unpause, help)
        
        ##### FIXME - this is not very pythonic. How can I do this without the messy
        # if statements? pause and unpause need to set special local variables
        # This is awful, you need to know what each code is! Not readable. :(
        # pause
        if myKeyHandler.sendCommand == -2:
            pause = True
            displayOff = True
            usrMessages.addMsg(myKeyHandler.msgType+str(msgTime.timeNow()), myKeyHandler.displayMsg)

        # unpause
        if myKeyHandler.sendCommand == -3:
            pause = False
            displayOff = False
            usrMessages.delAllMsg(myKeyHandler.msgType)
            
        # help
        if myKeyHandler.sendCommand == -4:
            #FIXME - hackish way of dealing with the fact that 
            # messages are one-liners and each message needs a unique id 
            # based on the epochtime in seconds serial number
            idCounter = 0.0
            for key in myKeyHandler.helpDict:
                usrMessages.addMsg(myKeyHandler.msgType+str(msgTime.timeNow()+idCounter), 
                                  key + ': ' + myKeyHandler.helpDict[key])
                # increment idCounter
                idCounter += .1 

    # check for changes in trackbar
    # update control panels and color swatches
    # update live frame 
    # calculate the mask for each channel

    # capture a frame and convert to HSV space
    myFrame.readFrame()
    ####FIXME move this into the class as part of self.readFrame
    myFrame.cvtHSV()

    # loop over each channel
    for color in channels:
        changes = False
        #make a copy of the color object for checking later 
        oldColor = color.copy()
        # check with the openCV HighGUI for changes on the trackbars
        color.syncTrackBars()

        # if the color range slider has moved update the hue range and the sliders
        if oldColor.colorRange != color.colorRange:
            color.setRangeDefault()
            cv2.setTrackbarPos(color.sliderHue[0], color.controlWinName, color.defaultRanges[color.colorRange][0])
            cv2.setTrackbarPos(color.sliderHue[1], color.controlWinName, color.defaultRanges[color.colorRange][1])
            changes=True

        # if the hue sliders have moved, update color swatch
        if (oldColor.lower[0] != color.lower[0]) or (oldColor.upper[0] != color.upper[0]):
            changes=True

        # update the windows if only if things have changed
        if changes:
            # update the color swatch attached to each control window
            updateControlWindow(color.controlWinName, color.midBGRcolor(), 
                        colorRange=color.defaultRanges[color.colorRange][2])

        # calculate the masks and pixel count 
        masks[color.name] = myFrame.calcMask(color.lower, color.upper)
        pixelCount[color.name] = myFrame.nonZero

    # calculate the ratio of colors in terms of a value between -1 and 1
    output.value = ratio(pixelCount[colorA.name], pixelCount[colorB.name])
    
    ####FIXME - the ws.connect should try every N cycles, not every cycle
    # check for websocket connection and send the video output value
    if ws.isConnected:
        ws.send(str(output.value))
        usrMessages.delMsg('error.socket')
    else:    
        # attempt a reconnection every N seconds (default is 3)
        ws.reconnect(3)
        usrMessages.addMsg('error.socket', 'socket not connected; attempting reconnect')
    
   
    # allow messages to be displayed for (N) seconds (refreshed every time a new key is pressed)
    if msgTime.hasElapsed(5):
        
        #clean out "info" messages after every update period has passed 
        usrMessages.delAllMsg('info')
 
    #update the pause screen every 5 seconds
    if displayOff and runTime.hasElapsed(5):
        runTime.setTime()
        # set pause to True to force an update of the pauseframe 
        ####FIXME this is a kludge. Find a better way to handle pausing?
        pause = True        
        
    # pause live updating and destroy some windows to save memory
    if pause and displayOff: 
        pauseFrame = myFrame.frame
        # destroy unneeded windows
        cv2.destroyWindow(channelDisplayName)
        # display messages from the message handler
        displayMessages(pauseFrame, usrMessages.msgList)
        cv2.imshow(liveDisplayName, pauseFrame)
        # unset pause condition
        pause = False       
             
    # calculate the resultant image for each channel
    # display live, result channels or pause message
    if not displayOff:
        # FIXME! Hack that does not use the class
        # I can't figure out how to do this using the class methods I have built.  
        # I would rather display each result frame from within a for loop like everything else
        # Unfortunately the mask is not recorded in the object so the last mask that is calculated
        # is saved and the result is based on ONLY that structure.
        
        # generates resultant frames with the following information:
        # Lower HSV, Upper HSV, indication of "direction" for paddle/bat in pong
        resA = cv2.bitwise_and(myFrame.frame, myFrame.frame, mask = masks[colorA.name])
        addText(resA, text = 'lower: ' + str(colorA.lower), textColor = colorA.midBGRcolor())
        addText(resA, text = 'upper: ' + str(colorA.upper), position = (10, 50), textColor = colorA.midBGRcolor())
        # direction of inflluence
        addText(resA, text = 'UP', position = (10, 100), textColor = colorA.midBGRcolor())
        
        resB = cv2.bitwise_and(myFrame.frame, myFrame.frame, mask = masks[colorB.name])
        addText(resB, text = 'lower: ' + str(colorB.lower), textColor = colorB.midBGRcolor())
        addText(resB, text = 'upper: ' + str(colorB.upper), position = (10, 50), textColor = colorB.midBGRcolor())
        # direction of influence
        addText(resB, text = 'DOWN', position = (10, 100), textColor = colorB.midBGRcolor())
       
    
        #cv2.imshow(colorA.name, resA)
        #cv2.imshow(colorB.name, resB)
        # join the resultant windows together horizontally (axis=1) and display
        cv2.imshow(channelDisplayName, np.concatenate((resA, resB), axis = 1))
        
        # add messages to the Live window 
        usrMessages.msgList['output value'] = 'ratio: ' + str(output.value)
        displayMessages(myFrame.frame, usrMessages.msgList)
        cv2.imshow(liveDisplayName, myFrame.frame)




# In[ ]:

myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

