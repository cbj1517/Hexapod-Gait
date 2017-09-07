import serComms as sc 
import conv
import time
import numpy as np
import initLegs as il
import math

def freeGait(legAngs, legMode, onGround, drctn, LRU):
    #drctn: x -> 0
    #       y -> 1
    #       rz -> 2
    
    #set variables
    
    
    diffMot = np.matrix([[5,0,0],           #rows are dx dy dz
                         [0,5,0],
                         [0,0,np.pi/20]])
    
    swingDiff = np.matrix([[5,0,0],         #rows are dx dy dz
                           [0,5,0],
                           [0,0,np.pi/20]])
    
    dF = [60,60,5*(np.pi/20)]               #[xF,yF,rzF]
    #dF = [60,80,5*(np.pi/20)]
    
    w = [np.pi/dF[0],np.pi/dF[1],np.pi/dF[2]]
    
##    dx = 5
##    dy = 5
##    rotz = np.pi/20

##    swingDx = 5    
##    swingDy = 5
##    swingRz = np.pi/20

    delF = -60  #max lift amplitude
    
##    yF = 60
##    xF = 50
##    rzF = (np.pi/20)*5
    
##    w = np.pi/xF
    
    maxRestrct = 0.8
    
    delta = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    curStatus = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    curDM = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    #curDy = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    #curRz = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    desZ = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    prevZ = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    prevLegMode = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    prevLegModeP1 = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    prevRestrct = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])

    feetPos = np.matrix([[0.0,0.0,0.0,0.0,0.0,0.0],
                         [0.0,0.0,0.0,0.0,0.0,0.0],
                         [0.0,0.0,0.0,0.0,0.0,0.0]])
    
    data = np.matrix([[0.00,0.00,0.00,0.00,0.00],
                      [0.00,0.00,0.00,0.00,0.00],
                      [0.00,0.00,0.00,0.00,0.00],
                      [0.00,0.00,0.00,0.00,0.00],
                      [0.00,0.00,0.00,0.00,0.00],
                      [0.00,0.00,0.00,0.00,0.00]])
    
    Q = '+'             #query move status
    s = 200
    x = 0
    g = 0
    
    #while x<250:
    while True:
        legMode, onGround, restrct, rstDiff, prevRestrct = checkLegMode(legMode, legAngs, onGround, prevRestrct, drctn, LRU)

        for k in range(0,6):
            
            if legMode[k,0] == 1 and onGround[k,0] == 0:    #if leg is in swing mode do sine trajectory
                if curDM[k,0] <= dF[drctn]:
                    desZ[k,0] = delF*np.sin(w[drctn]*curDM[k,0])
                    curDM[k,0] = curDM[k,0]+swingDiff[drctn,drctn]
                    dz = desZ[k,0]-prevZ[k,0]
                    
                    prevZ[k,0] = desZ[k,0]
                    if abs(dz) > 0:
                        delta[0,0] = -swingDiff[0,drctn]
                        delta[1,0] = -swingDiff[1,drctn]
                        delta[2,0] = dz
                        delta[3,0] = 0
                        delta[4,0] = 0
                        delta[5,0] = -swingDiff[2,drctn]
                        g = 1
                    else:
                        delta[0,0] = 0
                        delta[1,0] = 0
                        delta[2,0] = 0
                        delta[3,0] = 0
                        delta[4,0] = 0
                        delta[5,0] = 0                    
                else:
                    onGround[k,0] = 1
                    prevZ[k,0] = 0
                    curDM[k,0] = 0
                    
            elif legMode[k,0] == 0 and (restrct[k,0] < maxRestrct or prevLegMode[k,0] == 1 or rstDiff[k,0] < 0):
                delta[0,0] = diffMot[0,drctn]
                delta[1,0] = diffMot[1,drctn]
                delta[2,0] = 0
                delta[3,0] = 0
                delta[4,0] = 0
                delta[5,0] = diffMot[2,drctn]

                g = 2
            else:
                delta[0,0] = 0
                delta[1,0] = 0
                delta[2,0] = 0
                delta[3,0] = 0
                delta[4,0] = 0
                delta[5,0] = 0           

                g = 3
                
            legAngs[:,k] = conv.diffMotion(delta, legAngs, k)
            
            prevLegMode[k,0] = legMode[k,0]
            prevLegModeP1[k,0] = prevLegMode[k,0]
            
        data[:,0] = legMode
        data[:,1] = onGround
        data[:,2] = restrct            
        data[:,3] = rstDiff
        #data[:,4] = prevLegMode
        #print curStatus
        #print legMode
        #print onGround
        #print restrct
        #print data
        #print '----------------------'
        #time.sleep(0.5)
        Q = sc.tx(legAngs, s, 1)
        while Q is '+':
            Q = sc.tx(legAngs, s, 1)
            
        sc.tx(legAngs, s, 0)
        
        x += 1
        print x
###############################################################################################################################################################

def calcRestr(legAngs,legMode,drctn):
    totR = np.matrix([[0.000],[0.000],[0.000],[0.000],[0.000],[0.000]])

    legR = np.matrix([[0.000],[0.000],[0.000],[0.000],[0.000]])

    curFeetPos = np.matrix([[0.0,0.0,0.0,0.0,0.0,0.0],
                            [0.0,0.0,0.0,0.0,0.0,0.0],
                            [0.0,0.0,0.0,0.0,0.0,0.0]])

    q = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
    
    rstData = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

    qMax = np.matrix([[380.000],
                      [380.000],
                      [1.134],
                      [np.pi/2],
                      [1.92]])          #2.1
        
    qMin = np.matrix([[75.000],         #real min is 68 at extreme where legs actually collide
                      [75.000],
                      [-1.134],
                      [-np.pi/2],
                      [np.pi/3.5]])       #np.pi/3.5

    sigMax = np.matrix([[0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0]])

    sigMin = np.matrix([[0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0]])
    
    rSide = [0,1,5]
    rSM = np.matrix([[0,0,1,1,1],[0,1,1,1,1],[1,0,1,1,1]])
    lSM = np.matrix([[0,0,1,1,1],[1,0,1,1,1],[1,0,1,1,1]])
    #sM = np.matrix([[0,0,1,1,1],[0,0,1,1,1]])
         
    #precalculate smoothing factor for exp function
    for i in range(0,5):
        deltaQ = (qMax[i,0]+qMin[i,0])/2
        sigMax[i,0] = math.log(0.1)/(deltaQ-qMax[i,0])
        sigMin[i,0] = math.log(0.1)/(deltaQ-qMin[i,0])

    #calculate all feet positions wrt center of body
    for j in range(0,6):
        trans = conv.curFrame2(legAngs[:,j],j) 
        curFeetPos[:,j] = trans[0:3,3]

    #calculate restrictedness of all legs
    for k in range(0,6):

        if k == 0 or k == 1 or k == 5:
            sM = rSM[drctn,:]    #right side
        else:
            sM = lSM[drctn,:]    #left side
            
        ant = k+1
        post = k-1
            
        if ant>5:
            ant = 0
        if post<0:
            post = 5
            
        q[0,k] = math.sqrt((curFeetPos[0,k]-curFeetPos[0,ant])*(curFeetPos[0,k]-curFeetPos[0,ant])+(curFeetPos[1,k]-curFeetPos[1,ant])*(curFeetPos[1,k]-curFeetPos[1,ant]))
        q[1,k] = math.sqrt((curFeetPos[0,k]-curFeetPos[0,post])*(curFeetPos[0,k]-curFeetPos[0,post])+(curFeetPos[1,k]-curFeetPos[1,post])*(curFeetPos[1,k]-curFeetPos[1,post]))
        q[2,k] = legAngs[0,k]
        q[3,k] = legAngs[1,k]
        q[4,k] = legAngs[2,k]           
            
        for z in range(0,5):
            if q[z,k] > (qMax[z,0]+qMin[z,0])/2:
                legR[z,0] = math.exp(sigMax[z,0]*(q[z,k]-qMax[z,0]))
                
            elif q[z,k] <= (qMax[z,0]+qMin[z,0])/2:
                legR[z,0] = math.exp(sigMin[z,0]*(q[z,k]-qMin[z,0]))
        
        rstData[:,k] = legR
        #print legR
        #print'*******************'
        #totR[k,0] = sM[legMode[k,0],0]*legR[0,0] + sM[legMode[k,0],1]*legR[1,0] + sM[legMode[k,0],2]*legR[2,0] + sM[legMode[k,0],3]*legR[3,0] + sM[legMode[k,0],4]*legR[4,0]
        #totR[k,0] = sM[side,0]*legR[0,0] + sM[side,1]*legR[1,0] + sM[side,2]*legR[2,0] + sM[side,3]*legR[3,0] + sM[side,4]*legR[4,0]        
        totR[k,0] = sM[0,0]*legR[0,0] + sM[0,1]*legR[1,0] + sM[0,2]*legR[2,0] + sM[0,3]*legR[3,0] + sM[0,4]*legR[4,0]
    #print rstData
    return totR
###############################################################################################################################################################

def checkLegMode(legMode, legAngs, onGround, prevRestrct,drctn,LRU):
    maxRestrct = 0.8
    rstDiff = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    toSwing = [-1,-1,-1]
    cnt = 0
    swngCnt = 0
    
    restrct = calcRestr(legAngs,legMode,drctn)
   #LRU.reverse()
    
    #for k in range(0,6):
    for k in LRU:
        ant = k+1
        post = k-1
                    
        if ant>5:
            ant = 0
        if post<0:
            post = 5
            
        #calculate difference in current and previous restrictedness value to check in increasing or decreasing 
        rstDiff[k,0] = restrct[k,0] - prevRestrct[k,0]

        if legMode[k,0] == 0 and legMode[ant,0] == 0 and legMode[post,0] == 0 and rstDiff[k,0] >= 0:
            #change to swing mode
            legMode[k,0] = 1
            onGround[k,0] = 0
            toSwing[swngCnt] = cnt
##            #update LRU
##            z = LRU.pop(cnt)
##            LRU.append(z)
            swngCnt += 1
            
        elif legMode[k,0] == 1 and onGround[k,0] == 1:
            #change to stance mode
            legMode[k,0] = 0
             
            
        prevRestrct[k,0] = restrct[k,0]
        cnt += 1

    #update LRU
    #LRU.reverse()
    for i in range(0,3):
        if toSwing[i] != -1:
            z = LRU.pop(toSwing[i])
            LRU.append(z)
   #print LRU
    return (legMode,onGround,restrct,rstDiff,prevRestrct)
