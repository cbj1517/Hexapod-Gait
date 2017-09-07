import ik
import numpy as np
import conv as c
import serComms as sc
import initLegs as il

d = np.matrix([[0],[0],[40],[0],[0],[0]])

legAngs = il.setTo90()
##curTrans = np.matrix([[0, 0, 0, 0],
##                      [0, 0, 0, 0],
##                      [0, 0, 1, 0],
##                      [0, 0, 0, 1]])

Tcur = c.curFrame(legAngs[:,0],0)
deltaM = np.matrix([[0, -d[5], d[4], d[0]],
                        [d[5], 0, -d[3], d[1]],
                        [-d[4], d[3], 0, d[2]],
                        [0, 0, 0, 0]])
        
dT = deltaM*Tcur

legAngs[:,0] = ik.ik(dT[0:3,3], legAngs[0,0], legAngs[1,0], legAngs[2,0], 0)
Tcur = c.curFrame(legAngs[:,3],3)
deltaM = np.matrix([[0, -d[5], d[4], d[0]],
                        [d[5], 0, -d[3], d[1]],
                        [-d[4], d[3], 0, d[2]],
                        [0, 0, 0, 0]])
        
dT = deltaM*Tcur

legAngs[:,3] = ik.ik(dT[0:3,3], legAngs[0,3], legAngs[1,3], legAngs[2,3], 3)

sc.tx(legAngs,250,0)
#newAng = ik.ik(dU, a1, a2, a3)

