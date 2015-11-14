#!/usr/local/bin/python
#NOTE: You will have to update the ip address in index.html

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import random

class MainHandler(tornado.web.RequestHandler):

  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):

  connections = set()

  def check_origin(self, origin):
    return True

  def open(self):
    print 'connection opened...'
    self.write_message("The server says: 'Hello'. Connection was accepted.")
    self.connections.add(self)

  def on_message(self, message):
    foo = random.random()
    #self.write_message(message)
    #self.send(message)
    print 'received:', message
    [con.write_message(message) for con in self.connections]
    #for con in self.connections:
    #  self.write_message(message)


  def send(self, message):
    self.write_message(message)

  def on_close(self):
    print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
  application.listen(9000)
  tornado.ioloop.IOLoop.instance().start()

