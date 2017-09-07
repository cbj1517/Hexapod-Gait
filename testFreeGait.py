import serComms as sc 
import conv
import time
import numpy as np
import initLegs as il
import math
import restrict

delta = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
onGround = np.matrix([[0], [1], [0], [1], [0], [1]])
legMode = np.matrix([[1], [0], [1], [0], [1], [0]])

LRU = [1,3,5,0,2,4] #may need to prime this based on legs' starting state
Q = '+'             #query move status
s = 200


legAngs = il.setTo90()
time.sleep(2)

#drctn: x -> 0
#       y -> 1
#       rz -> 2

restrict.freeGait(legAngs, legMode, onGround, 0, LRU)
