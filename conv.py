import numpy as np
import ik
import time

def ang2pwm(T):
    #maximum and minimum pwm values
    pwm = np.zeros((3,6))
    maxPWM = 2000
    minPWM = 1000
    m = 286.48 

    pwm[0,0] = (m*T[0,0])+1500
    pwm[1,0] = (m*T[1,0])+1430
    pwm[2,0] = (m*T[2,0])+1475
    pwm[0,1] = (m*T[0,1])+1500
    pwm[1,1] = (m*T[1,1])+1500
    pwm[2,1] = (m*T[2,1])+1500
    pwm[0,2] = (m*T[0,2])+1500
    pwm[1,2] = (m*T[1,2])+1500
    pwm[2,2] = (m*T[2,2])+1500
    pwm[0,3] = (m*T[0,3])+1500
    pwm[1,3] = (m*T[1,3])+1500
    pwm[2,3] = (m*T[2,3])+1500
    pwm[0,4] = (m*T[0,4])+1570
    pwm[1,4] = (m*T[1,4])+1480
    pwm[2,4] = (m*T[2,4])+1500
    pwm[0,5] = (m*T[0,5])+1500
    pwm[1,5] = (m*T[1,5])+1500
    pwm[2,5] = (m*T[2,5])+1500
    
    #i = m*T
    #a = np.matrix([[1500, 1450, 1500, 1500, 1570, 1500], [1430, 1500, 1500, 1500, 1480, 1500], [1475, 1500, 1500, 1500, 1500, 1500]])
    #matrix of converted values
    #pwm = i+a

    #check for too high and too low servo values
    for elem in np.nditer(pwm, op_flags=['readwrite']):
        if elem > 1975:
            elem[...] = 1975
        elif elem < 1150:
            elem[...] = 1150
    
    return pwm

################################################################################

def curFrame(a,i):
    
    l1 = 42
    l2 = 101
    l3 = 106
    D = 0

    b2l = (i)*(np.pi/3)

    fuT0 = np.matrix([[np.cos(b2l), -np.sin(b2l), 0, D*np.cos(b2l)],
                      [np.sin(b2l), np.cos(b2l), 0, D*np.sin(b2l)],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    f0T1 = np.matrix([[np.cos(a[0, 0]), 0, np.sin(a[0, 0]), l1*np.cos(a[0, 0])],
                      [np.sin(a[0, 0]), 0, -np.cos(a[0, 0]), l1*np.sin(a[0, 0])],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

    f1T2 = np.matrix([[np.cos(a[1, 0]), np.sin(a[1, 0]), 0, l2*np.cos(a[1, 0])],
                      [np.sin(a[1, 0]), -np.cos(a[1, 0]), 0, l2*np.sin(a[1, 0])],
                      [0, 0, -1, 0],
                      [0, 0, 0, 1]])

    f2T3 = np.matrix([[np.cos(a[2, 0]), -np.sin(a[2, 0]), 0, l3*np.cos(a[2, 0])],
                      [np.sin(a[2, 0]), np.cos(a[2, 0]), 0, l3*np.sin(a[2, 0])],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    curTrans = fuT0*f0T1*f1T2*f2T3
    
    return curTrans
################################################################################

def curFrame2(a,i):
    
    l1 = 42
    l2 = 101
    l3 = 106
    D = 96

    b2l = (i)*(np.pi/3)

    fuT0 = np.matrix([[np.cos(b2l), -np.sin(b2l), 0, D*np.cos(b2l)],
                      [np.sin(b2l), np.cos(b2l), 0, D*np.sin(b2l)],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    f0T1 = np.matrix([[np.cos(a[0, 0]), 0, np.sin(a[0, 0]), l1*np.cos(a[0, 0])],
                      [np.sin(a[0, 0]), 0, -np.cos(a[0, 0]), l1*np.sin(a[0, 0])],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

    f1T2 = np.matrix([[np.cos(a[1, 0]), np.sin(a[1, 0]), 0, l2*np.cos(a[1, 0])],
                      [np.sin(a[1, 0]), -np.cos(a[1, 0]), 0, l2*np.sin(a[1, 0])],
                      [0, 0, -1, 0],
                      [0, 0, 0, 1]])

    f2T3 = np.matrix([[np.cos(a[2, 0]), -np.sin(a[2, 0]), 0, l3*np.cos(a[2, 0])],
                      [np.sin(a[2, 0]), np.cos(a[2, 0]), 0, l3*np.sin(a[2, 0])],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    curTrans = fuT0*f0T1*f1T2*f2T3
    
    return curTrans
################################################################################

def diffMotion(delta, curLegAngs, i):
    
    (r,c) = curLegAngs.shape
    if (r != 3) and (c != 6):
        print 'leg angle matrix is not 3x6'
        return


    dx = -delta[0]
    dy = -delta[1]
    dz = -delta[2]
    delx = -delta[3]
    dely = -delta[4]
    delz = -delta[5]
    
    totDx = 0.000
    totDy = 0.000
    totDz = 0.000
    totDelx = 0.000
    totDely = 0.000
    totDelz = 0.000

    transDiv = 100.00
    rotDiv = 100.00

    lAng = curLegAngs[:,i]
    
    Tcur = curFrame(lAng, i)

    while (np.absolute(totDx) < np.absolute(dx)) or (np.absolute(totDy) < np.absolute(dy)) or (np.absolute(totDz) < np.absolute(dz)) or (np.absolute(totDelx) < np.absolute(delx)) or (np.absolute(totDely) < np.absolute(dely)) or (np.absolute(totDelz) < np.absolute(delz)):

        if np.absolute(totDx) < np.absolute(dx):
            dTx = dx/transDiv
            totDx = totDx +dTx
        else:
            dTx = 0

        if np.absolute(totDy) < np.absolute(dy):
            dTy = dy/transDiv
            totDy = totDy +dTy
        else:
            dTy = 0

        if np.absolute(totDz) < np.absolute(dz):
            dTz = dz/transDiv
            totDz = totDz +dTz
        else:
            dTz = 0
            
        if np.absolute(totDelx) < np.absolute(delx):
            delTx = delx/rotDiv
            totDelx = totDelx +delTx
        else:
            delTx = 0

        if np.absolute(totDely) < np.absolute(dely):
            delTy = dely/rotDiv
            totDely = totDely +delTy
        else:
            delTy = 0

        if np.absolute(totDelz) < np.absolute(delz):
            delTz = delz/rotDiv
            totDelz = totDelz +delTz
        else:
            delTz = 0

        deltaM = np.matrix([[0, -delTz, delTy, dTx],
                            [delTz, 0, -delTx, dTy],
                            [-delTy, delTx, 0, dTz],
                            [0, 0, 0, 0]])
        
        dT = deltaM*Tcur

        lAng = ik.ik(dT[0:3,3], lAng[0,0], lAng[1,0], lAng[2,0], i)

        Tnew = Tcur + dT
        Tcur = Tnew
            
    return lAng
