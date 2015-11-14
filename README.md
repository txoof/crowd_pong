# crowd_pong
These scripts output a string of values between 1 and -1 on a web socket for 
controling a pong-like game using relative ratios of two colors visible to a web-cam.

**crowd_pong_video_capture**
Requirements: 
  * OpenCV 2.4 (On OS X: brew tap homebrew/science; brew install opencv)
  * Python 2.7 (On OS X: brew install python27)
  * OpenCV python bindings (pip install opencv)
  * numpy python module (pip install numpy)
  * websocket python module (pip install websocket-client)
  * tornado websocket echo server (pip install tornado[all]

Function:
Captures frames from a live video stream and provides a method for selecting from
two different colors. The relative ratio of colorA to colorB affects the output of a 
value between -1 and 1. The greater proportion of one color over the other affects
the velocity of the pong bat. The output value is sent as a message to a local
websocket server that rebroadcasts.  The game interface listens on 
ws://localhost/9000/ws.

The video capture script provides a live view and two masked views to show sampled
colorA and colorB.  The script also provides two sets of controls for fine-tuning the
color range, hue and saturation limits for each color.

  Control panels:
  Hue (+/-): general selected color range 
  S (+): saturation of color (darker colors have a higer saturation value)
  V (+/-): value of color (brigter colors have a higher value)
  CR: Preset color range to help quickly choose colors

  Note: Due to a bug in the OpenCV 2.4/Python 2.7 implementation that causes the 
  controls to be shuffled in an order that depends on the characters in the names,
  the control panels have less than ideal names.

Issues:
Absolutely no error trapping. Extreemly brittle.
Crashes when an another websocket client disconnects

**tornado-websocket-server**
Requirements:
  * Python 2.7
  * tornado python module (pip install tornado[all])

Function:
Websocket server that listens on ws://localhost/9000/ws for messages and then 
rebroadcasts incoming messages to all connected clients.

Issues:
Causes video client to crash when a websocket client disconnects; requires a restart
of video client and websocket server.
Load newSock.html to view output

**write_to_websocket**
Requirements:
  * Python 2.7
  * websocket-client (pip install websocket-client)

Fucntion: 
Test client for sending simulated output to websocket server.  

Issues:
Crashes when another websocket client disconnects.
