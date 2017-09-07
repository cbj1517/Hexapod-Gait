import conv as C
import msvcrt
import numpy as np
import serComms as sc

def RPY(legAngs):
    delta = np.matrix([[0.00], [0.00], [0.00], [0.00], [0.00], [0.00]])
    s = 250
    motion = 0
    
    while motion != -1:
        #get direction
        input_char = msvcrt.getch()
        
        if input_char.upper() == 'Q': 
            delta[0] = 5
            delta[1] = 0
            delta[2] = 0
            delta[3] = 0
            delta[4] = 0
            delta[5] = 0
            motion = 1
                
        elif input_char.upper() == 'W': 
            delta[0] = 0
            delta[1] = 5
            delta[2] = 0
            delta[3] = 0
            delta[4] = 0
            delta[5] = 0
            motion = 1
            
        elif input_char.upper() == 'E': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 5
            delta[3] = 0
            delta[4] = 0
            delta[5] = 0
            motion = 1
            
        elif input_char.upper() == 'R': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 0
            delta[3] = np.pi/20
            delta[4] = 0
            delta[5] = 0
            motion = 1

        elif input_char.upper() == 'T': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 0
            delta[3] = 0
            delta[4] = np.pi/20
            delta[5] = 0
            motion = 1
                
        elif input_char.upper() == 'Y': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 0
            delta[3] = 0
            delta[4] = 0
            delta[5] = np.pi/20
            motion = 1               
        elif input_char.upper() == 'A': 
            delta[0] = -5
            delta[1] = 0
            delta[2] = 0
            delta[3] = 0
            delta[4] = 0
            delta[5] = 0
            motion = 1
                
        elif input_char.upper() == 'S': 
            delta[0] = 0
            delta[1] = -5
            delta[2] = 0
            delta[3] = 0
            delta[4] = 0
            delta[5] = 0
            motion = 1
            
        elif input_char.upper() == 'D': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = -5
            delta[3] = 0
            delta[4] = 0
            delta[5] = 0
            motion = 1
            
        elif input_char.upper() == 'F': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 0
            delta[3] = -np.pi/20
            delta[4] = 0
            delta[5] = 0
            motion = 1

        elif input_char.upper() == 'G': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 0
            delta[3] = 0
            delta[4] = -np.pi/20
            delta[5] = 0
            motion = 1
                
        elif input_char.upper() == 'H': 
            delta[0] = 0
            delta[1] = 0
            delta[2] = 0
            delta[3] = 0
            delta[4] = 0
            delta[5] = -np.pi/20
            motion = 1
            
        elif input_char.upper() == 'X': 
            motion = -1            
        else:
            motion = 0

        if motion > 0:
            for i in range(0,6):
                legAngs[:,i] = C.diffMotion(delta,legAngs,i)
                
            sc.tx(legAngs, s, 0)
    
    return legAngs
