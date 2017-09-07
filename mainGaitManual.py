import serComms as sc 
import conv
import time
import numpy as np
import initLegs as il
import math
import restrict
import gaitManual as gm

JS = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])

legAngs = il.setTo90()
time.sleep(2)

JS[0,0] = 20
JS[1,0] = 0
JS[2,0] = 60
JS[5,0] = np.pi/12 #np.pi/10

gm.gait(legAngs,JS)
