import random
import pandas as pd
from cryptography.fernet import Fernet
import os


class Passwort_Manager:
    def __init__(self):
        self.userName=""
        self.loggedin=False

        self.userSeed=""
        self.userFileName=""
        self.key=""
        self.fernetObj= Fernet

        self.KeysPath=str(os.path.dirname( __file__ )+"\\Keys")
        self.UserDirPath=str(os.path.dirname( __file__ )+"\\User")

        self.CSVasList= pd
        


    def __loadKey(self):
        self.key=""
        for x in os.listdir(self.KeysPath):
            
            if(str(self.userFileName+".key")==x):
                with open(self.KeysPath+"/"+x,"r") as f:
                    self.key = f.read()

        if(self.key ==""):
            print("PWM: Error, User nicht gefunden")


    def __checkUserexistence(self, userName):
        self.__setUserSeed(userName)
        for x in os.listdir(self.UserDirPath):
            if(x==str(userName+".usr")):
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
            print("PWM: Username oder passowrd Falsch!")
            return False


    #Call to Logout
    def logout(self):
        self.loggedin=False
        self.userName=""

        self.userSeed=""
        self.userFileName=""
        self.key=""
        self.fernetObj=""

    #Call to Register
    def registerNewUser(self, userName, password,email):
        self.__setUserSeed(userName)
        if(self.__checkUserexistence(userName)==False):
            self.key = Fernet.generate_key()
            #Key File
            with open(str(self.KeysPath+"/"+self.userFileName+".key"),"wb") as file:
                file.write(self.key)

            self.__setFernetobj()
            #_id=0
            encryptplatform = self.fernetObj.encrypt(b"self")
            encryptUserName=self.fernetObj.encrypt(bytes(userName,encoding="utf-8"))
            encryptPassword= self.fernetObj.encrypt(bytes(password,encoding="utf-8"))
            encryptEmail = self.fernetObj.encrypt(bytes(email, encoding="utf-8"))
            #User File
            with open(str(self.UserDirPath+"/"+userName+".usr"),"w") as file:
                file.write("PlatformName:Username:Password:Email:SecurityKey:Telephon:Link:ImgPath\n"
                           +encryptplatform.decode()+":"+encryptUserName.decode()+":"+encryptPassword.decode()+":"+encryptEmail.decode())
            return True
            #self.login(userName,password)
        else:
            print("PWM: User Existiert Bereits")
            return False
            #self.logout()



    def __setFernetobj(self):
        self.__loadKey()
        self.fernetObj=Fernet(self.key)


    def __setUserSeed(self, userName):
        self.userSeed = userName
        self.__setUserFileName()

    def __setUserFileName(self):
        random.seed(self.userSeed)
        self.userFileName=random.random()
        self.userFileName = str(self.userFileName).replace("0.","")


    def translate(self,item):
        self.__setFernetobj()
        return self.fernetObj.decrypt(item).decode()
    def getAllPasswords(self):
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
                print("PWM: new IMGPath: ",self.translate(self.CSVasList.loc[_id]["ImgPath"]))

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
            path = str(self.UserDirPath + "/" + self.userSeed+ ".usr")
            self.CSVasList = pd.read_csv(path, sep=":")
            print("PWM: Read CSV")

    def __WriteCSV(self):
        path = str(self.UserDirPath + "/" + self.userSeed + ".usr")
        self.CSVasList.to_csv(path,index=False, sep=":")
        print("PWM: Write CSV")
