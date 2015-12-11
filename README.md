#crowd pong
Installation Guide for Crowd Pong server and Glowsticks game engine.
Crowd Pong (c) by Aaron Ciuffo

 _______  _______  _______           ______          _______  _______  _        _______ 
(  ____ \(  ____ )(  ___  )|\     /|(  __  \        (  ____ )(  ___  )( (    /|(  ____ \
| (    \/| (    )|| (   ) || )   ( || (  \  )       | (    )|| (   ) ||  \  ( || (    \/
| |      | (____)|| |   | || | _ | || |   ) |       | (____)|| |   | ||   \ | || |      
| |      |     __)| |   | || |( )| || |   | |       |  _____)| |   | || (\ \) || | ____ 
| |      | (\ (   | |   | || || || || |   ) |       | (      | |   | || | \   || | \_  )
| (____/\| ) \ \__| (___) || () () || (__/  )       | )      | (___) || )  \  || (___) |
(_______/|/   \__/(_______)(_______)(______/        |/       (_______)|/    )_)(_______)
                                                                                   
                             

1. Install PyCharm (Nice GUI wrapper for Python)
	- This will make installing the packages less of a tarball-ache, especially if you hate tar.gz etc.

2. Go to http://www.github.com/txoof/crowd_pong/ and download all files/folders.
	- Save it to a nice directory like ...\Steve's Documents\crowd_pong-master\

3. Open Pycharm and open the directory you created (...\crowd_pong-master\) which contains all the python files.

4. Now you need to install the individual packages, in PyCharm go: File>Settings>Project:"project name">Project Interpreter

5. Press the green + button on the right side of the list.You will be able to add packages through this menu.

6. Add the following packages, need to use the package ID:

	Package ID		      Package name

	pip			            PIP - a package manager, very useful	
	cv2			            OpenCV2 - an webcam/image processing library
	tornado			        Tornado - a websocket library to communicate with the web game engine
	websocket-client	 Websocket client library, needed for debugging and testing
	numpy			          NumPy - additional maths functionality in python

7. Save everything and restart. Just 'cause.
 _______  _______  _______  _______ 
(  ____ \(  ___  )(       )(  ____ \
| (    \/| (   ) || () () || (    \/
| |      | (___) || || || || (__    
| | ____ |  ___  || |(_)| ||  __)   
| | \_  )| (   ) || |   | || (      
| (___) || )   ( || )   ( || (____/\
(_______)|/     \||/     \|(_______/
                                    
_________ _        _______ _________ _______           _______ __________________ _______  _        _______ 
\__   __/( (    /|(  ____ \\__   __/(  ____ )|\     /|(  ____ \\__   __/\__   __/(  ___  )( (    /|(  ____ \
   ) (   |  \  ( || (    \/   ) (   | (    )|| )   ( || (    \/   ) (      ) (   | (   ) ||  \  ( || (    \/
   | |   |   \ | || (_____    | |   | (____)|| |   | || |         | |      | |   | |   | ||   \ | || (_____ 
   | |   | (\ \) |(_____  )   | |   |     __)| |   | || |         | |      | |   | |   | || (\ \) |(_____  )
   | |   | | \   |      ) |   | |   | (\ (   | |   | || |         | |      | |   | |   | || | \   |      ) |
___) (___| )  \  |/\____) |   | |   | ) \ \__| (___) || (____/\   | |   ___) (___| (___) || )  \  |/\____) |
\_______/|/    )_)\_______)   )_(   |/   \__/(_______)(_______/   )_(   \_______/(_______)|/    )_)\_______)
                                                                                                            





+-------------------------+                                   +-------------------------------------------+
|                         |   Websocket Values -1.0^=x^=1.0   |                                           |
|  Python Webcam Processor+---------------------------------->+  OpenRC Game Engine                       |
|                         |                                   |                                           |
|  cp_video_sample.py     |   Default websocket address:      |  http://openrc.chronopunch.com/pongV2.0/  |
|                         |    ws://localhost:9000/ws         |                                           |
|                         |                                   |                                           |
|                         |                                   |                                           |
+-------------------------+                                   +-------------------------------------------+


1. Open Pycharm and open the directory you created in the INSTALLATION ABOVE (...\crowd_pong-master\) which contains all the python files.

2. Run tornado-websocket-server.py and ensure no error codes are shown. If you have issues here, it may be a firewall problem.

3. Ensure your USB webcam is plugged in, or your laptop has a working integrated webcam.

4. Run cp_video_capture.py

5. Your webcam should start up and you should see four live windows.
	- UP - Green Controls
	- DOWN - Yellow Controls
	- Up & Down (side-by-side screens from left-to-right, the Up and Down masks)
	- Live

In the Up and down control windows (default to yellow/green) the easiest way to start is with the color range slide at the bottom.
You should do this while watching the Up & Down window. The idea is to show both colour glow sticks next to one another.
You want to tweak the HUE controls such that they are as small as possible, while giving good results.
Good results: - The green glowstick is clearly visible (within Up&Down) on the left screen and the yellow glowstick is clearly visible on the right screen.
		- The hue range is small, maybe about 40 difference between Hue- and Hue+.
		- When you hide the glpowsticks, no other light is showing. The NonZero px count should be 0 for both screens.

6. Once you have got the controls nice and happy, hit Shift+s. It should save the controls. Shift+l loads them. Or just write down the ranges.

7. Open the Game Engine. If you have an internet connection, go to http://openrc.chronopunch.com/pongV2.0/

8. Modify the websocket address if necessary, otherwise hit 'GO' with your mouse.

9. The game controls should be instantly responding to the camera view.

10. Protip: If the camera sees an equal amount of green/yellow, the bat won't move.
	Hide one colour (e.g. behind your back), and show the other to move the paddle. If you want the paddle to slow down, then try showing both colours.




 _______  _______  _        _______  _______  _______  _______    _        _______ _________ _______  _______ 
(  ____ )(  ____ \( \      (  ____ \(  ___  )(  ____ \(  ____ \  ( (    /|(  ___  )\__   __/(  ____ \(  ____ \
| (    )|| (    \/| (      | (    \/| (   ) || (    \/| (    \/  |  \  ( || (   ) |   ) (   | (    \/| (    \/
| (____)|| (__    | |      | (__    | (___) || (_____ | (__      |   \ | || |   | |   | |   | (__    | (_____ 
|     __)|  __)   | |      |  __)   |  ___  |(_____  )|  __)     | (\ \) || |   | |   | |   |  __)   (_____  )
| (\ (   | (      | |      | (      | (   ) |      ) || (        | | \   || |   | |   | |   | (            ) |
| ) \ \__| (____/\| (____/\| (____/\| )   ( |/\____) || (____/\  | )  \  || (___) |   | |   | (____/\/\____) |
|/   \__/(_______/(_______/(_______/|/     \|\_______)(_______/  |/    )_)(_______)   )_(   (_______/\_______)


Crowd Pong (c) by Aaron Ciuffo

Crowd Pong is licensed under a Creative Commons Atrribution-ShareAlike 3.0 Unported Licenses

You should have received a copy of the license along with this work. If not, see http://creativecommons.org/licenses/by/3.0/.

These scripts output a string of values between 1 and -1 on a web socket for controling a pong-like game using relative ratios of two colors visible to a web-cam.

Scripts provided as both ipython notebooks and python scripts.

crowd_pong_video_capture Requirements:

OpenCV 2.4 (On OS X: brew tap homebrew/science; brew install opencv)
Python 2.7 (On OS X: brew install python27)
OpenCV python bindings (pip install opencv)
numpy python module (pip install numpy)
websocket python module (pip install websocket-client)
tornado websocket echo server (pip install tornado[all]
Function: Captures frames from a live video stream and provides a method for selecting from two different colors. The relative ratio of colorA to colorB affects the output of a value between -1 and 1. The greater proportion of one color over the other affects the velocity of the pong bat. The output value is sent as a message to a local websocket server that rebroadcasts. The game interface listens on ws://localhost/9000/ws.

The video capture script provides a live view and two masked views to show sampled colorA and colorB. The script also provides two sets of controls for fine-tuning the color range, hue and saturation limits for each color.

Control panels: Hue (+/-): general selected color range S (+): saturation of color (darker colors have a higer saturation value) V (+/-): value of color (brigter colors have a higher value) CR: Preset color range to help quickly choose colors

See cp-instructions.txt for more information.

tornado-websocket-server Requirements:

Python 2.7
tornado python module (pip install tornado[all])
Function: Websocket server that listens on ws://localhost/9000/ws for messages and then rebroadcasts incoming messages to all connected clients.

write_to_websocket Requirements:

Python 2.7
websocket-client (pip install websocket-client)
Fucntion: Test client for sending simulated output to websocket server.
	



