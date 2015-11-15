
# coding: utf-8

# In[7]:

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time

class WSHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
         self.connections.add(self)
         print 'New connection was opened'
         self.write_message("Conn!")

    def on_message(self, message):
        print 'Got :', message
        self.write_message("Received: " + message)
        #[con.write_message('hi') for con in connections]


    def on_close(self):
        self.connections.remove(self)
        print 'Conn closed...'
        
application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(9000)
  tornado.ioloop.IOLoop.instance().start()


# In[ ]:



