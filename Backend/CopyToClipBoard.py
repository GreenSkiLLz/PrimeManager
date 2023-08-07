import os
import subprocess

class CopyToClipBoard:
    def __init__(self):
        self.Command1 = "ECHO | SET /P="
        self.Command2 = "| CLIP"

    def copy(self,text):
        print("Copy: ",text)
        try:
            subprocess.call(str("ECHO | SET /P="+text+"| CLIP"),shell=True)
            #subprocess.run(str(self.pathTempFile+"\\temp.bat"))
        except:
            print("Error while Copying")