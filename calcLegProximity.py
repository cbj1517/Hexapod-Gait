import serComms as sc 
import conv
import time
import numpy as np
import initLegs as il
import math

curFeetPos = np.matrix([[0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0]])
k = 0
ant = 1

legAngs = il.setTo90()

#move legs 0 and 1 close together and calc porximity value
legAngs[0,0] = 1.134
legAngs[0,1] = -1.134

#sc.tx(legAngs,200,0)
#time.sleep(200)

for i in range(0,2):
    trans = conv.curFrame2(legAngs[:,i],i) 
    curFeetPos[:,i] = trans[0:3,3]

minProx = math.sqrt((curFeetPos[0,k]-curFeetPos[0,ant])*(curFeetPos[0,k]-curFeetPos[0,ant])+(curFeetPos[1,k]-curFeetPos[1,ant])*(curFeetPos[1,k]-curFeetPos[1,ant]))

print minProx

#move legs 0 and 1 far apart and calc porximity value
legAngs[0,0] = -1.134
legAngs[0,1] = 1.134

for i in range(0,2):
    trans = conv.curFrame2(legAngs[:,i],i) 
    curFeetPos[:,i] = trans[0:3,3]

maxProx = math.sqrt((curFeetPos[0,k]-curFeetPos[0,ant])*(curFeetPos[0,k]-curFeetPos[0,ant])+(curFeetPos[1,k]-curFeetPos[1,ant])*(curFeetPos[1,k]-curFeetPos[1,ant]))

print maxProx
