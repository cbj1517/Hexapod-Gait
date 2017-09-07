import serComms as sc 
import conv
import time
import msvcrt
import numpy as np

def initGait(legAngs, legPairs, delta, joyS):
    for pair in range(0,2):
        for i in range(0,3):
            leg = legPairs[pair, i]
            #swing and raise one leg at a time to initial position
            if pair == 0:
                delta[0,0] = joyS[0,0]/2.00
                delta[1,0] = joyS[1,0]/2.00
                delta[2,0] = -60
                delta[3,0] = joyS[3,0]/2.00
                delta[4,0] = joyS[4,0]/2.00
                delta[5,0] = joyS[5,0]/2.00                
            else:
                delta[0,0] = -joyS[0,0]/2.00
                delta[1,0] = -joyS[1,0]/2.00
                delta[2,0] = -60
                delta[3,0] = -joyS[3,0]/2.00
                delta[4,0] = -joyS[4,0]/2.00
                delta[5,0] = -joyS[5,0]/2.00
            
            legAngs[:,leg] = conv.diffMotion(delta, legAngs, leg)
            sc.tx(legAngs, 250, 0)

            #place leg back on the ground after it has reached its final position
            delta[0,0] = 0
            delta[1,0] = 0
            delta[2,0] = 60
            delta[3,0] = 0
            delta[4,0] = 0
            delta[5,0] = 0
            
            legAngs[:,leg] = conv.diffMotion(delta, legAngs, leg)
            sc.tx(legAngs, 250, 0)
            
    return legAngs

###########################################################################################
#Changed to just lift on first and last two phases - 8/10

#joyS is x, y, z, dx, dy, dz
def gait(legAngs, JS):
    #init gait params
    s = 200
    k = 0
    kmax = 4.00
    steps = 50
    legPairs = np.matrix([[0, 2, 4],[1, 3, 5]])
    delta = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    liftPair = 0
    motion = 0
    init = 0
    stride = 30
    lift = 60
    turn = np.pi/6
    Q = '+'             #query move status
    joyS = JS
    seqComp = False
    
    while True:
        #print motion
        while seqComp == False:
            for pair in range(0,2):
                for i in range(0,3):
                    leg = legPairs[pair, i]
                    if joyS[0,0]!=0 or joyS[1,0]!=0 or joyS[5,0]!=0:
                        if k < 1 or k >= (kmax):
                            if pair == liftPair:
                                delta[0,0] = 0
                                delta[1,0] = 0
                                delta[2,0] = -1*joyS[2,0]*(((0.500-(k/kmax))))
                                delta[3,0] = 0
                                delta[4,0] = 0
                                delta[5,0] = 0
                            else:
                                delta[0,0] = 0
                                delta[1,0] = 0
                                delta[2,0] = 0
                                delta[3,0] = 0
                                delta[4,0] = 0
                                delta[5,0] = 0
                                    
                        elif k >= 1 and k < (kmax):
                            if pair == liftPair:
                                delta[0,0] = -1*joyS[0,0]/(kmax-2.00)
                                delta[1,0] = -1*joyS[1,0]/(kmax-2.00)
                                delta[2,0] = -1*joyS[2,0]*(((0.500-(k/kmax))))
                                delta[3,0] = -1*joyS[3,0]/(kmax-2.00)
                                delta[4,0] = -1*joyS[4,0]/(kmax-2.00)
                                delta[5,0] = -1*joyS[5,0]/(kmax-2.00)
                            else:
                                delta[0,0] = joyS[0,0]/(kmax-2.00)
                                delta[1,0] = joyS[1,0]/(kmax-2.00)
                                delta[2,0] = 0
                                delta[3,0] = joyS[3,0]/(kmax-2.00)
                                delta[4,0] = joyS[4,0]/(kmax-2.00)
                                delta[5,0] = joyS[5,0]/(kmax-2.00)
##                        else:
##                            #stop leg from moving
##                            delta[0,0] = 0
##                            delta[1,0] = 0
##                            delta[2,0] = 0
##                            delta[3,0] = 0
##                            delta[4,0] = 0
##                            delta[5,0] = 0
                             
                    legAngs[:,leg] = conv.diffMotion(delta, legAngs, leg)
                        
            Q = sc.tx(legAngs, s, 1)
            while Q is '+':
                Q = sc.tx(legAngs, s, 1)    

            sc.tx(legAngs, s, 0)
                
            if joyS[0,0]!=0 or joyS[1,0]!=0 or joyS[5,0]!=0 or joyS[2,0]!=0:
                k += 1
                if k > kmax:
                    #seqComp = True
                    k = 0
                    if liftPair == 1:
                        liftPair = 0
                    else:
                        liftPair += 1
                else:
                    seqComp = False
                        
    #Put legs back down here upon exiting while loop
    #legAngs = il.setTo90()
    return legAngs
