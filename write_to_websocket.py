
# coding: utf-8

# In[1]:

from websocket import create_connection
import random
import time
ws = create_connection("ws://localhost:9000/ws")

def rando():
    time.sleep(0.4)
    num = (random.random()*2)-1
    return str(num)

while True:
    ws.send(rando())
    #result = ws.recv()
ws.close


# In[ ]:

print random.random()
print type (str(random.random()))


# In[ ]:



