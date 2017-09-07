import numpy as np
import serComms as sc
import time
def setTo90():
    T =  np.matrix([[0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2]])

    sc.tx(T,250,0)
    time.sleep(0.25)
    return T
