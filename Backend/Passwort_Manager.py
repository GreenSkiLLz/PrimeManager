import random
import pandas as pd
from cryptography.fernet import Fernet
import time
import os
import threading


class Passwort_Manager:
    def __init__(self):
        self.userName=""
        self.loggedin=False

        self.userSeed=""
        self.userKeyFileName=""
        self.userSaveFileName =""
        self.key=""
        self.fernetObj= Fernet

        
        ##Depricated
        #self.KeysPath=str(os.path.dirname( __file__ )+"\\Keys")
        #self.UserDirPath=str(os.path.dirname( __file__ )+"\\User")

        ## Use this Path in future!!!
        #Appdata Path for user for R/W access
        user = os.getlogin()
        self.local_appdata_path = os.path.join('C:\\', 'Users', user, 'AppData', 'Local','PrimeManager')
        self.KeysPath=os.path.join(self.local_appdata_path,"Keys")
        self.UserDirPath=os.path.join(self.local_appdata_path,"User")
        
        if not os.path.exists(self.local_appdata_path):
            os.makedirs(self.local_appdata_path)
        if not os.path.exists(self.KeysPath):
            os.makedirs(self.KeysPath)
        if not os.path.exists(self.UserDirPath):
            os.makedirs(self.UserDirPath)
            



        self.CSVasList= pd

        # TFA Variables
        self.tfaUser=""
        self.currenttfaCode=""
        self.currentEmailCode=""
        self.verifyEmailSendingStatus=""

    def __loadKey(self):
        self.key=""
        for x in os.listdir(self.KeysPath):
            
            if(str(self.userKeyFileName+".key")==x):
                with open(self.KeysPath+"/"+x,"r") as f:
                    self.key = f.read()

        if(self.key ==""):
            print("PWM: Error, User nicht gefunden")


    def __checkUserexistence(self, userName):
        self.__setUserSeed(userName)
        for x in os.listdir(self.UserDirPath):
            if(x==str(self.userSaveFileName+".usr")):
                return True
        return False
    
    
    #Find User for TFA
    def forgottPassword_Step1(self,userName):
        if self.__checkUserexistence(userName):
            self.tfaUser = userName
            return True
        return False

    #Generate Code and send call EmailThread start Function
    def forgottPassword_Step2(self):
        random.seed(time.process_time())
        tfacode=[random.randrange(10) for i in range(8)]
        self.currenttfaCode = "".join(str(e) for e in tfacode)
        print(self.currenttfaCode)
        email = self.__forgottPassword_GetEmail()
        self.__forgottPassword_EmailThread(self.currenttfaCode,email)
        return email

    def forgottPassword_setPW(self,newpw):
        Password_ = self.fernetObj.encrypt(bytes(newpw, encoding="utf-8")).decode()
        self.CSVasList.loc[0]["Password"] = Password_
        self.__WriteCSV()
        self.logout()

    #Compare Codes
    def forgottPassword_Compare(self,code):
        if(self.currenttfaCode == code):
            return True
        return False
    #Cancle TFA and delete Code
    def forgottPassword_Cancle(self):
        print("PWM: Cancle TFA")
        self.currenttfaCode=""
        self.logout()

    #Start EMail Thread and Send Code
    def __forgottPassword_EmailThread(self,code,email):
        # args: pwd, recipient, code
        recipient = email
        t1 =threading.Thread(target= self.send_TFA, args=["zvwfcfudbjqqouam",recipient,code])
        t1.start()
    
    # Gets called before EmailThread is started
    def __forgottPassword_GetEmail(self):
        self.__setUserSeed(self.tfaUser)
        self.__setFernetobj()
        self.__readCSVAndSetCSVlist()
        email = self.fernetObj.decrypt(self.CSVasList.loc[0]["Email"]).decode()
        return email

    #Actual Thread
    def send_TFA(self, pwd, recipient, code):
        import smtplib
        user = "infoprimemanager@gmail.com"
        text = str("Here is you requested Code to reset your Password:\n\n\t"+code+
                "\n\nIf you did not requiest this code, you can safely ignore this E-Mail\n"+
                "Your Password can't be changed without this code!\n\n"+
                "Kind regards,\nYour Prime Manager\n\n\n-This E-Mail was generated automatically, please do NOT Reply."
                )
        
        FROM = user
        TO = recipient if isinstance(recipient, list) else [recipient]
        SUBJECT = "Prime Manager, reset your Password"
        TEXT = text
        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print ('successfully sent the mail')
        except:
            print ("failed to send mail")


    def validateEmail_step1(self):
        if not self.loggedin:
            return
        
        random.seed(time.process_time())
        validationCode=[random.randrange(10) for i in range(8)]
        self.currentEmailCode = "".join(str(e) for e in validationCode)
        print("PMG: ",self.currentEmailCode)
        
        t1 =threading.Thread(target= self.send_Email_TFA, args=["zvwfcfudbjqqouam",self.getCurrentEmail(),self.currentEmailCode])
        t1.start()

    
    def vlaidateEmail_finish(self):
        self.currentEmailCode=""
        self.verifyEmailSendingStatus=""

    def validateEmail_step2(self,code):
        if not self.loggedin:
            return False
        
        if code == self.currentEmailCode:
            print("PMG: Correct Validation Code: ",code)
            self.editProfile(col="SecurityKey",value=str(code))
            self.vlaidateEmail_finish()
            return True
        
        return False


    def send_Email_TFA(self, pwd, recipient, code):
        import smtplib
        user = "infoprimemanager@gmail.com"
        text = str("To validate your E-Mail enter the following Code into the validation textfield:\n\n\t"+code+
                "\n\nIf you did not requiest this code, you can safely ignore this E-Mail.\n"+
                "Your Email can't get validated without this code!\n\n"+
                "Kind regards,\nYour Prime Manager\n\n\n-This E-Mail was generated automatically, please do NOT Reply."
                )
        
        FROM = user
        TO = recipient if isinstance(recipient, list) else [recipient]
        SUBJECT = "Prime Manager, validate your Email"
        TEXT = text
        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            self.verifyEmailSendingStatus=True
            print ('successfully sent the mail')
        except:
            self.verifyEmailSendingStatus=False
            print ("failed to send mail")


    #Check String for Password
    def checkPW(self, password):
        if self.loggedin:
            if self.fernetObj.decrypt(self.CSVasList.loc[0]["Password"]) == bytes(password, encoding="utf-8"):
                return True

        return False
    
    #Call to Login
    def login(self, username,password):
        if(self.loggedin==True):
            print("PWM: Bereits Angemeldet")
        elif(self.__checkUserexistence(username)):
            self.__setUserSeed(username)
            self.__setFernetobj()
            self.__readCSVAndSetCSVlist()

            if (self.fernetObj.decrypt(self.CSVasList.loc[0]["Password"]) == bytes(password, encoding="utf-8")):
                
                self.__setUserSeed(username)
                self.__setFernetobj()
                self.loggedin = True
                self.userName = username

                print("PWM: Login")
                return True

            else:
                print("PWM: Username oder passowrd Falsch!")
                return False

        else:
            print(self.fernetObj.decrypt(self.CSVasList.loc[0]["Password"]))
            print("PWM: Username oder passowrd Falsch! 01")
            return False


    #Call to Logout
    def logout(self):
        self.loggedin=False
        self.userName=""

        self.userSeed=""
        self.userKeyFileName=""
        self.key=""
        self.fernetObj=""
        self.CSVasList=""
        
        self.tfaUser =""
        self.currentEmailCode=""
        self.verifyEmailSendingStatus=""

    #Call to Register
    def registerNewUser(self, userName, password,email):
        self.__setUserSeed(userName)
        if(self.__checkUserexistence(userName)==False):
            self.key = Fernet.generate_key()
            #Key File
            with open(str(self.KeysPath+"/"+self.userKeyFileName+".key"),"wb") as file:
                file.write(self.key)

            self.__setFernetobj()
            #_id=0
            encryptplatform = self.fernetObj.encrypt(b"self")
            encryptUserName=self.fernetObj.encrypt(bytes(userName,encoding="utf-8"))
            encryptPassword= self.fernetObj.encrypt(bytes(password,encoding="utf-8"))
            encryptEmail = self.fernetObj.encrypt(bytes(email, encoding="utf-8"))
            encryptImg = self.fernetObj.encrypt(b"Img\\sicher.png")
            #User File
            with open(str(self.UserDirPath+"/"+self.userSaveFileName+".usr"),"w") as file:
                file.write("PlatformName:Username:Password:Email:SecurityKey:Telephon:Link:ImgPath\n"
                           +encryptplatform.decode()+":"+encryptUserName.decode()+":"+encryptPassword.decode()+":"+encryptEmail.decode()+"::::"+encryptImg.decode())
            return True
            #self.login(userName,password)
        else:
            print("PWM: User Existiert Bereits")
            return False
            #self.logout()


    #EditProfile
    #PlatformName;Username;Password;Email;SecurityKey;Telephon;Link;ImgPath
    def editProfile(self,col="",value=""):
        if self.loggedin:

            #platform_ = self.fernetObj.encrypt(bytes(platform, encoding="utf-8")).decode()
            #self.CSVasList.loc[0]["Email"] = [platform_,userName_,Password_,eMail_,securityKey_,telephon_,link_,imgPath_]

            if col=="":
                return
            
            elif col=="Username":
                userName_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["Username"] = userName_

            elif col=="Password":
                Password_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["Password"] = Password_

            elif col=="Email":
                eMail_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["Email"] = eMail_

            elif col=="SecurityKey":
                securityKey_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["SecurityKey"] = securityKey_

            elif col=="Telephon":
                telephon_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["Telephon"] = telephon_

            elif col=="Link":
                link_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["Link"] = link_

            elif col=="ImgPath":
                imgPath_ = self.fernetObj.encrypt(bytes(value, encoding="utf-8")).decode()
                self.CSVasList.loc[0]["ImgPath"] = imgPath_
        
            self.__WriteCSV()

    
    def getAvatarPath(self):
        if not self.loggedin:
            return "Img\\sicher.png"
        try:
            if not pd.isnull(self.CSVasList.loc[0]["ImgPath"]):
                return self.fernetObj.decrypt(self.CSVasList.loc[0]["ImgPath"]).decode()
        except:
            return "Img\\sicher.png"
            
        return "Img\\sicher.png"
    

    def getCurrentEmail(self):
        if not self.loggedin:
            return False

        return self.fernetObj.decrypt(self.CSVasList.loc[0]["Email"]).decode()
    

    def getEmailValidation(self):
        if not self.loggedin:
            return False
        
        if pd.isnull(self.CSVasList.loc[0]["SecurityKey"]) or self.fernetObj.decrypt(self.CSVasList.loc[0]["SecurityKey"]).decode() =="":
            return False
        else:
            return True
        
        
    def __setFernetobj(self):
        self.__loadKey()
        self.fernetObj=Fernet(self.key)


    def __setUserSeed(self, userName):
        self.userSeed = userName
        self.__setUserFileName()

    def __setUserFileName(self):
        random.seed(self.userSeed)
        self.userKeyFileName=random.random()
        self.userKeyFileName = str(self.userKeyFileName).replace("0.","")
        random.seed(self.userKeyFileName)
        self.userSaveFileName = random.random()
        self.userSaveFileName = str(self.userSaveFileName).replace("0.","")
        print(self.userKeyFileName,self.userSaveFileName)


    def translate(self,item):
        self.__setFernetobj()
        return self.fernetObj.decrypt(item).decode()
    
    def getAllPasswords(self):
        if(len(self.CSVasList)>0):
            return self.CSVasList
        self.__readCSVAndSetCSVlist()
        return self.CSVasList


    #Call to add new Password
    #CSV:  ID;PlatformName;Username;Password;Email;SecurityKey;Telephon;Link;ImgPath
    #Is Fast
    def add_password(self,platform,userName="",Password="",eMail="",securityKey="",telephon="",link="",imgPath=""):
        if(self.loggedin):
            self.__readCSVAndSetCSVlist()
            #ID = len(self.CSVasList)
            encryptplatform = self.fernetObj.encrypt(bytes(platform,encoding="utf-8"))
            encryptUserName=self.fernetObj.encrypt(bytes(userName,encoding="utf-8"))
            encryptPassword= self.fernetObj.encrypt(bytes(Password,encoding="utf-8"))
            encryptEmail = self.fernetObj.encrypt(bytes(eMail,encoding="utf-8"))
            encryptSecurityKey = self.fernetObj.encrypt(bytes(securityKey, encoding="utf-8"))
            encryptTelephon = self.fernetObj.encrypt(bytes(telephon, encoding="utf-8"))
            encryptLink = self.fernetObj.encrypt(bytes(link, encoding="utf-8"))
            encryptImgPath = self.fernetObj.encrypt(bytes(imgPath, encoding="utf-8"))

            df={"PlatformName": encryptplatform.decode('utf-8'),
                 "Username": encryptUserName.decode('utf-8'),
                 "Password": encryptPassword.decode('utf-8'),
                 "Email": encryptEmail.decode('utf-8'),
                 "SecurityKey": encryptSecurityKey.decode('utf-8'),
                 "Telephon": encryptTelephon.decode('utf-8'),
                 "Link": encryptLink.decode('utf-8'),
                 "ImgPath": encryptImgPath.decode('utf-8')}
            df= pd.DataFrame([df])

            self.CSVasList = pd.concat([self.CSVasList,df])
            self.__WriteCSV()



    def edit_password(self, _id,platform="", userName="", Password="", eMail="", securityKey="", telephon="", link="",imgPath=""):
        if self.loggedin:
            self.__readCSVAndSetCSVlist()
            _id=int(_id)
            print("PWM: Editing ID: ",_id, " IMG: ",imgPath)
            if _id != 0 and _id < len(self.CSVasList.index):
                platform_ = self.fernetObj.encrypt(bytes(platform, encoding="utf-8")).decode()
                userName_ = self.fernetObj.encrypt(bytes(userName, encoding="utf-8")).decode()
                Password_ = self.fernetObj.encrypt(bytes(Password, encoding="utf-8")).decode()
                eMail_ = self.fernetObj.encrypt(bytes(eMail, encoding="utf-8")).decode()
                securityKey_ = self.fernetObj.encrypt(bytes(securityKey, encoding="utf-8")).decode()
                telephon_ = self.fernetObj.encrypt(bytes(telephon, encoding="utf-8")).decode()
                link_ = self.fernetObj.encrypt(bytes(link, encoding="utf-8")).decode()
                imgPath_ = self.fernetObj.encrypt(bytes(imgPath, encoding="utf-8")).decode()
                self.CSVasList.loc[_id] = [platform_,userName_,Password_,eMail_,securityKey_,telephon_,link_,imgPath_]
                self.__WriteCSV()
                #print("PWM: new IMGPath: ",self.translate(self.CSVasList.loc[_id]["ImgPath"]))

    #Call to get Password from ID
    #Not Used in KivyUI
    def get_password(self,_id):
        _id=_id+1
        return self.CSVasList[_id]

    def delete_password(self,_id):
        if self.loggedin:
            self.__readCSVAndSetCSVlist()
            _id = int(_id)
            if _id < len(self.CSVasList.index):
                self.CSVasList.drop([_id], axis=0, inplace=True)
            self.__WriteCSV()

    def __readCSVAndSetCSVlist(self):
        path = os.path.join(self.UserDirPath ,str(self.userSaveFileName+ ".usr"))
        self.CSVasList = pd.read_csv(path, sep=":")
   
        print("PWM: Read CSV")

    def __WriteCSV(self):
        self.__setUserSeed(self.userName)
        path = str(self.UserDirPath + "/" + self.userSaveFileName + ".usr")
        self.CSVasList.to_csv(path,index=False, sep=":")
        print("PWM: Write CSV")
