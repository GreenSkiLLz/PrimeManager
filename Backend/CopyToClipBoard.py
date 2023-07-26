import os
import subprocess

class CopyToClipBoard:
    def __init__(self):
        self.pathTempFile=os.path.dirname( __file__ )
        self.winPath = self.pathTempFile.replace("\\","/")
        self.Command1 = "ECHO | SET /P="
        self.Command2 = "| CLIP"

    def copy(self,text):
        print("Copy: ",text)
        with open(self.pathTempFile+"\\temp.bat", "w") as f:
            f.write(str(self.Command1+text+self.Command2))
        try:
            subprocess.call(str("ECHO | SET /P="+text+"| CLIP"),shell=True)
            #subprocess.run(str(self.pathTempFile+"\\temp.bat"))
        except:
            print("Error while Copying")

        with open(self.pathTempFile+"\\temp.bat", "w") as f:
            f.write(str(self.Command1+""+self.Command2))