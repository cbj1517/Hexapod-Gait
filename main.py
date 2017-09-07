import gait
import time
import RPY
import initLegs as il

choose = 0

legAngs = il.setTo90()

while True:
    if choose == 0:
        legAngs = RPY.RPY(legAngs)
        legAngs = il.setTo90()
        choose = 1
    elif choose == 1:
        legAngs = gait.gait(legAngs)
        legAngs = il.setTo90()
        choose = 0
    

