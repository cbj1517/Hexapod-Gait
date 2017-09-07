import numpy as np
import math
import conv

#use this to calculate the min and max radius of the workspace for various
#values of height of the hexapod body
L0 = 42
L1 = 101
L2 = 106
phi = 1.396
lamdaMin =0
lamdaMax = 1.6581

H = 79.5

rMax = L0 + L1 + math.sqrt(math.pow(L2,2)-math.pow(H,2))
rMin = L0 + L1*np.cos(phi)+L2*np.cos(phi+lamdaMin)

print 'rMin = ' + str(rMin)
print 'rMax = ' + str(rMax)
