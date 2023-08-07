from Passwort_Manager import Passwort_Manager
import pandas as pd

pm = Passwort_Manager()

#pm.registerNewUser("admin","admin","admin")
#pm.login("admin","admin")
#print(pm.loggedin)
#pm.add_password("Google")
#pm.edit_password(1,"C")
#pm.delete_password(2)
#df = pm.getAllPasswords()

#print(len(df.index))

import os
import random

random.seed("GreenSkiLLz")
userFileName=random.random()
userFileName = str(userFileName).replace("0.","")
random.seed(userFileName)
userSaveFileName = random.random()
userSaveFileName = str(userSaveFileName).replace("0.","")

print(userFileName,userSaveFileName)