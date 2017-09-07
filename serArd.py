import serial
import numpy as np
def serArd():
    
    ard = serial.Serial('COM4', 115200)
    s = ard.readline()

    l = []
    x = np.matrix([[1],[1],[1]])
    for i in s.split():
        try:
            l.append(float(i))

        except ValueError:
            pass

    l = np.array(l)
    
    return l


            
