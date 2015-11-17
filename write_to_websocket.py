
# coding: utf-8

# In[ ]:

from websocket import create_connection
import random
import time

def formatOutput(msg):
    '''format a message with the appropriate pre/postfix'''
    #pre/post fix
    pf = '#'
    return pf + msg + pf
    

def randReal():
    time.sleep(0.4)
    num = (random.random()*2)-1
    return str(num)

def randInt():
    return str(random.randrange(0, 10))

def outScore():
    '''output the a score'''
    return formatOutput('SCORE: AI:' + randInt()+ '; Human:' + randInt())

def outPoint():
    '''output who just scored'''
    entity = random.randrange(0, 2)
    if entity == 0:
        output = formatOutput('POINT: AI')
    else:
        output = formatOutput('POINT: Human')
    return output

def outGameOver():
    '''output game-over status'''
    entity = random.randrange(0, 2)
    if entity == 0:
        output = formatOutput('GAMEOVER: Winner: AI')
    else:
        output = formatOutput('GAMEOVER: Winner: Human')
    return output


def randomOutput():
    possibleOutput  = {'0': outScore, '1': outPoint, '2': outGameOver}
    choice = str(random.randrange(0, 3))
    
    output = possibleOutput[choice]()
    
    return output

ws = create_connection("ws://localhost:9000/ws")
count = 0 
while True:
    # simulate sending video capture data
    ws.send(randReal())
    
    #simulate sending game results
    if random.randrange(0, 100) < 10:
        ws.send(randomOutput())

# well, this is rather pointless.  We never get here.
ws.close





# In[ ]:

for i in range(0, 100):
    print random.randrange(0, 3)

