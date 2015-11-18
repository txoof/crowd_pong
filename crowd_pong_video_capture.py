
# coding: utf-8

# In[4]:

import cv2
import numpy as np
import re
import copy
from websocket import create_connection
import websocket


#Classes
class outputValue:
    '''class for recording the float output value from the video sampling'''
    def __init__(self):
        self.value = 0.0
        
class loopHalt(Exception): pass
        
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

        
    def copy(self):
        '''make a duplicate object'''
        return copy.deepcopy(self)
    
    # Ask martin about this again
    def hasChanged(self):
        '''compare self to a copy and if it has changed'''
        pass

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

class webSocket:
    '''create a web socket connection
    url - complete url in the form of ws://host:<port>/path
    socket - websocket object
    isConnected - boolean'''
    def __init__(self, url):
        self.url = url
        self.isConnected = False
        self.socket = self.connect
        
    def connect(self):
        try:
            self.socket = websocket.create_connection(self.url)
            if self.socket.connected:
                self.isConnected = True
        except Exception, e:
            self.isConnected = False
            
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
        self.foo = 'foobar'
        
    def addMsg(self, msgID, msg):
        '''add messages to the list
        msgID - unique identifyer for message
        msg - message to be displayed'''
        self.msgList[msgID] = msg
    
    def delMsg(self, msgID):
        '''remove messages to the list
        msgID - unique identifyer for message'''
        if msgID in self.msgList:
            del self.msgList[msgID]
        else:
            pass

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
    
    
    def calibration(self):
        self.sendCommand = '5'
        self.displayMsg = self.helpDict[self.keyPressCHR] + ': Code ' + self.sendCommand
        self.msgType = info
        
    def printHelp(self):
        for key in self.helpDict:
            print key, self.helpDict[key]
    
    def restartPoint(self):
        self.sendCommand= '4'
        self.displayMsg = self.helpDict[self.keyPressCHR] + ': Code ' + self.sendCommand
        #self.displayMsg = 'Restart Point: Code ' + self.sendCommand
        self.msgType = 'info'
    
    def quit(self):
        self.functionCall = doNothing()
        raise loopHalt
        
    def restartGame(self):
        self.sendCommand = '3'
        self.displayMsg = self.helpDict[self.keyPressCHR] + ': Code ' + self.sendCommand
        #self.displayMsg = 'Restart Game: Code ' + self.sendCommand
        self.msgType = 'info'
        
    def credits(self):
        self.sendCommand = '6'
        self.displayMsg = self.helpDict[self.keyPressCHR] + ': Code ' + self.sendCommand
        self.msgType = 'info'
        
    def pauseDisplay(self):
        pass
    
    def unpauseDisplay(self):
        pass
    

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
        return(0)
    if countA > countB:
        # give a negative number
        percent=-1*((countA-countB)/float(countA))
    if countA < countB:
        #give a positve number
        percent=1*((countB-countA)/float(countB))
    
    if  .2 > percent > -.2:
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
    pass


# In[5]:


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

# init the list of important display messages
usrMessages = msgHandler()

# create a connection to the web socket handler object
ws = webSocket(socketURL)

# Count the loops for updating the paused display
runningLoop = 0
# frequency to update and clean displayed user messages
updateRate = 100

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
    

    
##### TESTING
myKeyHandler = keyHandler()
keyPress = None
    
# begin looping until user quits
while True:     
   
    ####FIXME - time to make this a class/sub?
    # capture key presses & act on them
    keyPress = cv2.waitKey(1)
    
    # capture keypresses and handel them
    # halt on loopHalt exception
    try:
        myKeyHandler.keyInput(keyPress)
        #execute the functioncall that has been set based on keyPress
        myKeyHandler.functionCall
    except loopHalt:
        # clean up on exception
        myFrame.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        break
    
    if myKeyHandler.sendCommand is not None:
        sendCommand(command = myKeyHandler.sendCommand, websocket = ws)
        usrMessages.addMsg(myKeyHandler.msgType+str(runningLoop), myKeyHandler.displayMsg)
    
    
    #FIXME add exception for dealing with this
    # pause live display, destroy windows, display pause message
    if keyPress & 0xFF == ord ('p'):
        pause = True
        displayOff = True
        usrMessages.addMsg('pause.1', 'Live display paused')
        usrMessages.addMsg('pause.2', '\'u\': unpause; shift+\'q\' to quit')
    
    # unpause live display
    if keyPress & 0xFF == ord ('u'):
        pause = False
        displayOff = False
        usrMessages.delMsg('pause.1')
        usrMessages.delMsg('pause.2')
                
    if keyPress & 0xFF == ord ('h'):
        usrMessages.addMsg('info.'+str(runningLoop+.1), 'R: restart game')
        usrMessages.addMsg('info.'+str(runningLoop+.2), 'P: restart point')
        usrMessages.addMsg('info.'+str(runningLoop+.3), 'C: restart calibration')
        usrMessages.addMsg('info.'+str(runningLoop+.4), 'Z: return to credits')
        usrMessages.addMsg('info.'+str(runningLoop+.5), 'Q: quit')
        usrMessages.addMsg('info.'+str(runningLoop+.6), 'Z: return to credits')
        usrMessages.addMsg('info.'+str(runningLoop+.7), 'p: pause live display')
    
    #reset the keypress variable
    keyPress=False    

    # check for changes in trackbar
    # update control panels and color swatches
    # update live frame 
    # calculate the mask for each channel

    # capture a frame and convert to HSV space
    myFrame.readFrame()
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
    
    # check for websocket connection and send the video output value
    if ws.isConnected:
        ws.send(str(output.value))
        usrMessages.delMsg('socket.err')
    else:
        ws.connect()
        usrMessages.addMsg('socket.err', 'socket not connected; attemting reconnect')
    
    #FIXME move this into a sub?
    # update the pause screen and clean out old info messages
    if (runningLoop % updateRate == 0): 
        #clean out "info" messages after every update period has passed 
        for k in usrMessages.msgList.keys():
            regexp = 'info.*'
            m = re.search(regexp, k)
            if m is not None:
                usrMessages.delMsg(k)        
        
        #update the pause screen
        if displayOff:
            # set pause to True to force an update of the pauseframe 
            pause = True
            # reset the running loop 
            runningLoop = 0
            
    if runningLoop >= 1001:
        # reset to prevent an overflow
        runningLoop = 0
    
       
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
    
    #increment the loop counter (used to update user information)
    runningLoop += 1





# In[ ]:

myFrame.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:

class myClass:
    i = 3
    def __init__(self):
        self.eye = self.i
    def g(self):
        print self.i
        
myVar = myClass()
print myVar.eye


# In[ ]:

print dir(runningLoop)

