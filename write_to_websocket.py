
# coding: utf-8

# In[1]:

from websocket import create_connection
import random
import time
ws = create_connection("ws://localhost:9000/ws")

def randReal():
    time.sleep(0.4)
    num = (random.random()*2)-1
    return str(num)

def randInt():
  return str(random.randrange(0, 10))

count = 0 

while True:
    # prevent an overflow
    if count > 100000:
      count = 0
    ws.send(randReal())
    if count % 20 == 0:
      for i in range(1):
        ws.send('SCORE# AI:'+randInt()+'; Human:'+randInt()+'#')
    #result = ws.recv()
    count += 1
ws.close


# In[ ]:

print random.random()
print type (str(random.random()))


# In[ ]:



