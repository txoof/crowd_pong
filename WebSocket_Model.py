
# coding: utf-8

# In[ ]:

#Socket tester for python
import time
import cherrypy
import random
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

cherrypy.config.update({'server.socket_port': 9000})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class Root(object):
    @cherrypy.expose
    def index(self):
        return "<p style=\"font-family:Verdana\">Generating live red:green ratios and sending to JS web client...</p>"

    @cherrypy.expose
    def ws(self):
        # you can access the class instance through
        handler = cherrypy.request.ws_handler



class myHandler(WebSocket):
    def opened(self):
        # cherrypy.engine.publish('add-client', self.username, self)
        return "<p>Connection successful</p>"

    def received_message(self, message):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(message.data))
        while message.data != 99:
            RGratio = (2*random.random()-1)
            cherrypy.engine.publish('websocket-broadcast',TextMessage(str(RGratio)))
            time.sleep(0.4)
    def closed(self, code, reason="No reason... just closed."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))



cherrypy.quickstart(Root(), '/', config={'/ws': {'tools.websocket.on': True,
                                                 'tools.websocket.handler_cls': myHandler}})

'''while True:
    cherrypy.engine.publish('websocket-broadcast',TextMessage("Hellow wuld"))
    time.sleep(10)'''


# In[1]:

get_ipython().magic(u'who')


# In[ ]:



