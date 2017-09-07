import serial
import numpy as np
import initLegs as IL

def moveJ(angle, leg, joint):
    ssc32 = serial.Serial('COM9', 115200)

    #set up look up table for servo number based on leg(column) and joint(row)
    servo = np.matrix([[0, 17, 20, 23, 6, 3],[1, 18, 21, 24, 7, 4],[2, 19, 22, 25, 8, 5]])

    #angle should be given in radians
    pwm =(286.48*angle)+1500
    
    ssc32.write('#'+str(servo[joint,leg])+'P'+str(pwm)+'T'+str(350)+'\r')
