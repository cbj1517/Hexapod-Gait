import serArd as ser
import numpy as np
import conv
import initLegs as il
import serComms as sc
import gait
import time
import moveJoint as mj
import restrict as r
import math

##legAngs = il.setTo90()
##legAngs[2,:] = (85.00/180)*np.pi
##
##legMode = np.matrix([[0],
##                     [1],
##                     [0],
##                     [1],
##                     [0],
##                     [1]])
##totR = r.calcRestr(legAngs,legMode)
##
##print totR

il.setTo90()

theta = np.matrix([[-np.pi/12],[0],[np.pi/2]])
sc.snglLeg(theta, 300, 3)
