#Function will perform inverse kinematics one leg of the robot.
#Takes in differential change vector WRT hip, and current joint angles of legs.

import numpy as np

def ik(dU, a1, a2, a3, i):

    (r,c) = dU.shape
    if (r != 3) and (c != 1):
        print 'dU matrix is not 3x1'
        return
    
    l1 = 42         #link length 1 in mm
    l2 = 101        #link length 2 in mm
    l3 = 106        #link length 3 in mm

    ai = (i)*(np.pi/3)
    
    J = np.around(np.matrix([[(l1+np.cos(a2)*l2+l3*np.cos(a2-a3))*(-np.sin(a1)*np.cos(ai)-np.cos(a1)*np.sin(ai)), (-np.sin(a2)*l2-l3*np.sin(a2-a3))*(np.cos(a1)*np.cos(ai)-np.sin(a1)*np.sin(ai)), l3*np.sin(a2-a3)*(np.cos(a1)*np.cos(ai)-np.sin(a1)*np.sin(ai))],
                   [(l1+np.cos(a2)*l2+l3*np.cos(a2-a3))*(-np.sin(a1)*np.sin(ai)+np.cos(a1)*np.cos(ai)), (-np.sin(a2)*l2-l3*np.sin(a2-a3))*(np.cos(a1)*np.sin(ai)+np.sin(a1)*np.cos(ai)), l3*np.sin(a2-a3)*(np.cos(a1)*np.sin(ai)+np.sin(a1)*np.cos(ai))],
                   [0, l2*np.cos(a2)+l3*np.cos(a2-a3), -l3*np.cos(a2-a3)]]), decimals = 10)

    try:
        dT = np.linalg.inv(J)*dU
    except:
        print 'matrix at singularity'

    newAng = np.matrix([[a1], [a2], [a3]])+dT
    
    return newAng
