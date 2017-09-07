#Module will communicte serially with ssc32 servo board.
#Takes in joint angle matrix T, and speed variable s.

import serial
import conv as C
import time
import numpy as np

def tx(theta, s, i):
    Q = '-'
    try:
        #ssc32 = serial.Serial('/dev/ttyUSB0', 115200)
        ssc32 = serial.Serial('COM12', 115200)
    except:
        print 'ssc32 board NOT communicating!'
        
    (r,c) = theta.shape
    if (r != 3) and (c != 6):
        print 'Angle matrix is NOT 3x6!'
        return
    
    T = C.ang2pwm(theta)
    
    #delay = (s/1000)
    s = str(s)

    if i == 0:
        try:
            ssc32.write('#0P'+str(T[0,0])+'#1P'+str(T[1,0])+'#10P'+str(T[2,0])+'#17P'+str(T[0,1])+'#18P'+str(T[1,1])+'#19P'+str(T[2,1])+'#20P'+str(T[0,2])+'#21P'+str(T[1,2])+'#22P'+str(T[2,2])+'#23P'+str(T[0,3])+'#24P'+str(T[1,3])+'#25P'+str(T[2,3])+'#6P'+str(T[0,4])+'#7P'+str(T[1,4])+'#8P'+str(T[2,4])+'#3P'+str(T[0,5])+'#4P'+str(T[1,5])+'#5P'+str(T[2,5])+'T'+str(s)+'\r')
        except:
            print 'Serial write FAILED!'
    elif i == 1:
        try:
            ssc32.write('Q \r')
            Q = ssc32.read()
        except:
            print 'Serial write FAILED!'

    return Q
        

def snglLeg(theta, s, leg):
    srvPins = np.matrix([[0,17,20,23,6,3],[1,18,21,24,7,4],[2,19,22,25,8,5]])
    T = np.matrix([[0.00,0.00,0.00,0.00,0.00,0.00],[0.00,0.00,0.00,0.00,0.00,0.00],[0.00,0.00,0.00,0.00,0.00,0.00]])
    T[:,leg] = theta
    T = C.ang2pwm(T)
    #print T
    try:
        #ssc32 = serial.Serial('/dev/ttyUSB0', 115200)
        ssc32 = serial.Serial('COM12', 115200)
    except:
        print 'ssc32 board NOT communicating!'
        
    (r,c) = theta.shape
    if (r != 3) and (c != 1):
        print 'Angle matrix is NOT 3x1!'
        return
    #print T[1,leg]
    try:
        ssc32.write('#'+ str(srvPins[0,leg])+'P'+str(T[0,leg])+'#'+ str(srvPins[1,leg])+'P'+str(T[1,leg])+'#'+str(srvPins[2,leg])+'P'+str(T[2,leg])+'T'+str(s)+'\r')
    except:
        print 'Serial write FAILED!'  

def sndPWM(t1,t2,t3,s,leg):
    srvPins = np.matrix([[0,17,20,23,6,3],[1,18,21,24,7,4],[2,19,22,25,8,5]])
    try:
        #ssc32 = serial.Serial('/dev/ttyUSB0', 115200)
        ssc32 = serial.Serial('COM12', 115200)
    except:
        print 'ssc32 board NOT communicating!'
        
    try:
        ssc32.write('#'+ str(srvPins[0,leg])+'P'+str(t1)+'#'+ str(srvPins[1,leg])+'P'+str(t2)+'#'+str(srvPins[2,leg])+'P'+str(t3)+'T'+str(s)+'\r')
    except:
        print 'Serial write FAILED!'     








