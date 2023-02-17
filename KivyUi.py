from kivy.config import Config
from kivy.uix.image import Image
Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')
Config.set('graphics', 'minimum_width', '1366')
Config.set('graphics', 'minimum_height', '768')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'keyboard_mode', 'system')

#Comps needet for Building Exe
from kivy.uix.filechooser import FileChooserIconView
from kivymd.icon_definitions import md_icons
from kivymd.uix.card import MDCard
from kivymd.uix.slider import MDSlider
from kivymd.uix.recycleview import MDRecycleView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, ImageRightWidget, ThreeLineRightIconListItem
import win32timezone
#### 

import os
from Backend.CopyToClipBoard import CopyToClipBoard
from Backend.Password_Generator import Password_Generator
from Backend.Passwort_Manager import Passwort_Manager


class FilechooserPopup(Popup):
    def __init__(self, returnfunction, start, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.ret = returnfunction
        self.ids["filechooser"].path = str(start) + "\\Img"
        self.title = str("Add new Img here : " + str(start) + "\\Img")

    def chooseFileFileChosserPopup(self, fc, img):
        if fc.selection:
            img.source = str(fc.selection[0])
            self.ret(fc.selection[0])


class GeneratePasswordPopup_Pop(Popup):
    def __init__(self, returnfunction, **kwargs):
        super(Popup, self).__init__(**kwargs)
        self.returnfunction = returnfunction
        self.passwordGenerator = Password_Generator()
        self.currentpw = ""

    def generatePW(self, lb_generatedPW, slide_chars, cb_upperlower, cb_numbers, cb_symbols):
        generated = self.passwordGenerator.generatePassword(
            int(slide_chars.value),
            cb_upperlower.active,
            cb_numbers.active,
            cb_symbols.active)
        lb_generatedPW.text = generated

    def savePassword(self, obj):
        self.currentpw = obj.text
        self.currentpw = str(self.currentpw).replace(" ", "")
        obj.text = self.currentpw

    def returnpassword(self):
        self.returnfunction(str(self.currentpw))


class ListItem(ThreeLineRightIconListItem):
    def __init__(self, **kwargs):
        super(ListItem, self).__init__(**kwargs)
        self.listref = MainScreen()

        # Information
        self.id_ = ""
        self.platformName = ""
        self.userName = ""
        self.password = ""
        self.email = ""
        self.securityKey = ""
        self.phone = ""
        self.link = ""

        self.listitemimg = ObjectProperty(None)
        self.the_popup = ObjectProperty(None)

    # Function to get reference of ListItem when clicked on
    def sayHello(self):
        self.listref.loadIndexFromScrollList(self)

    def setIMG(self, path):
        if path != "":
            self.ids['listitemimg'].source = path

    def setid_(self, id_):
        self.id_ = id_

    def setPlatformName(self, text):
        self.platformName = text
        self.text = text

    def setUserName(self, username):
        self.userName = username
        self.secondary_text = "Username: " + username

    def setPassword(self, pw):
        self.password = pw

    def setEmail(self, email):
        self.email = email
        self.tertiary_text = "Email: " + email

    def setSecurityKey(self, securitykey):
        self.securityKey = securitykey

    def setPhoneNr(self, phone):
        self.phone = phone

    def setLink(self, link):
        self.link = link

    def get(self, what=""):
        if what == "IMG":
            return str(self.ids['listitemimg'].source)
        if what == "PLATFORMNAME":
            return self.platformName
        if what == "USERNAME":
            return self.userName
        if what == "PASSWORD":
            return self.password
        if what == "EMAIL":
            return self.email
        if what == "SECURITYKEY":
            return self.securityKey
        if what == "PHONE":
            return self.phone
        if what == "LINK":
            return self.link
        if what == "ID":
            return self.id_

        return ""


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.pm = Passwort_Manager()
        self.user = ObjectProperty(None)
        self.password = ObjectProperty(None)
        self.bt_forgotpassword = ObjectProperty(None)
        self.cb_rememberme = ObjectProperty(None)
        self.lines=""

        # Password Manager:
        self.app = MDApp.get_running_app()
    
    def on_enter(self, *args):
        if self.ids:
            self.loadRememberme()
        return super().on_enter(*args)


    def on_kv_post(self, base_widget):
        self.loadRememberme()

        return super().on_kv_post(base_widget)
    
    def loadRememberme(self):
        print('UI: Loading Login Page')
        with open("Backend\\Remember.me","r") as file:
            self.lines = file.readlines()
        if self.lines:
            if self.lines[0].strip() == "True":
                self.cb_rememberme.active = True
                self.user.text = self.lines[1]
                print("UI: Remember Me set to True")
            else:
                self.cb_rememberme.active = False
                print("UI: Remember Me set to False")

    def validateText(self):
        self.user.text = str(self.user.text).replace(" ", "")
        self.password.text = str(self.password.text).replace(" ", "")

    def login(self):
        # If Username not Available
        if self.user.text == "" or self.password.text == "":
            self.password.error = True
            self.password.helper_text = ("Wrong Username or Password")
            self.clearbeforeleave()
            return

        if self.app.pm.login(self.user.text, self.password.text):
            self.rememberMe()
            
            self.clearbeforeleave()
            Window.maximize()
            self.manager.current = 'mainscreen'
        
        #Error
        else:
            self.password.error = True
            self.password.helper_text = ("Wrong Username or Password")
            self.clearbeforeleave()
            return
        #Error
        return

    def rememberMe(self):
        print("UI: Remeber Me: ",self.cb_rememberme.active)
        newlines=[]
        if self.cb_rememberme.active:
            newlines.append("True")
            newlines.append(self.user.text)
        else:
            newlines.append("False")
            newlines.append("")
            
        with open("Backend\\Remember.me","w") as file:
            file.write(str(newlines[0]+"\n"+newlines[1]))


    def forgotPassword(self):
        print("UI: forgot password")
        self.clearbeforeleave()
        self.manager.current = 'tfa'

    def register(self):
        print("UI: register")
        self.clearbeforeleave()
        self.manager.current = 'register'

    def clearbeforeleave(self):
        self.user.text = ""
        self.password.text = ""


class Register(Screen):
    def __init__(self, **kwargs):
        super(Register, self).__init__(**kwargs)

        self.user = ObjectProperty(None)
        self.email = ObjectProperty(None)
        self.password = ObjectProperty(None)
        self.valpassword = ObjectProperty(None)

        # Password Manager:
        self.app = MDApp.get_running_app()

    def register(self):
        # Username is Empty
        if self.user.text == "":
            self.user.error = True
            self.user.helper_text = "Enter an Username"
            return

        # Email is Empty
        if self.email.text == "":
            self.email.error = True
            self.email.helper_text = "Enter an Email"
            return

        # Password is empty
        if self.password.text == "":
            self.password.error = True
            self.password.helper_text = "Enter an Password"
            return

        # Passwords are not the same
        if self.password.text != self.valpassword.text:
            self.valpassword.error = True
            self.valpassword.helper_text = "Password is not the same"
            self.valpassword.text = ""
            return

        # Username already Taken
        if not self.app.pm.registerNewUser(self.user.text, self.password.text, self.email.text):
            self.user.error = True
            self.user.helper_text = "Username already taken"
            return
        self.clearbeforeleave()
        self.manager.current = 'login'

    def validateText(self):
        self.user.text = str(self.user.text).replace(" ", "")
        self.password.text = str(self.password.text).replace(" ", "")
        self.valpassword.text = str(self.valpassword.text).replace(" ", "")
        self.email.text = str(self.email.text).replace(" ", "")

    def back(self):
        self.clearbeforeleave()
        self.manager.current = 'login'

    def clearbeforeleave(self):
        self.user.helper_text = ""
        self.email.helper_text = ""
        self.password.helper_text = ""
        self.valpassword.helper_text = ""
        self.user.text = ""
        self.email.text = ""
        self.password.text = ""
        self.valpassword.text = ""

#Step 2 TFA
class ForgotPassword(Screen):
    def __init__(self, **kwargs):
        super(ForgotPassword, self).__init__(**kwargs)
        
        self.app = MDApp.get_running_app()

        self.text_label=ObjectProperty(None)
        self.tfacode=ObjectProperty(None)
        self.newPassword=ObjectProperty(None)
        self.valNewPassword=ObjectProperty(None)
        self.validation_label = ObjectProperty(None)
        self.setpw = ObjectProperty(None)
    
    def clearbeforeleave(self):
        self.app.pm.forgottPassword_Cancle()
        self.tfacode.text = ""
        self.newPassword.text = ""
        self.valNewPassword.text = ""
        self.validation_label.text = "First enter the Code"
        self.setpw.disabled = True
        self.newPassword.disabled = True
        self.valNewPassword.disabled = True
        self.newPassword.hint_text_color_normal = [1, 99/255, 99/255,1]
        self.valNewPassword.hint_text_color_normal = [1, 99/255, 99/255,1]


    def validateText(self, obj):
        obj.text = str(obj.text).replace(" ","")

    def validatetfa(self):
        if len(self.tfacode.text) < 8:
            self.validation_label.text = "First enter the Code"
            self.newPassword.disabled = True
            self.valNewPassword.disabled = True
            self.newPassword.hint_text_color_normal = [1, 99/255, 99/255,1]
            self.valNewPassword.hint_text_color_normal = [1, 99/255, 99/255,1]

            self.setpw.disabled = True

        self.tfacode.text = str(self.tfacode.text).replace(" ","")

        if(len(self.tfacode.text)==8):
            if self.app.pm.forgottPassword_Compare(self.tfacode.text):
                self.validation_label.text = "Set new Password:"
                self.newPassword.disabled = False
                self.valNewPassword.disabled = False
                self.newPassword.hint_text_color_normal = [86/255, 197/255, 150/255, 1]
                self.valNewPassword.hint_text_color_normal = [86/255, 197/255, 150/255, 1]

                self.setpw.disabled = False
                print("Correct Code")
            else:
                print("Wrong Code")
                self.tfacode.error=True
                self.tfacode.helper_text=("WRONG CODE")
                self.validation_label.text = "Code is WRONG!"
                self.newPassword.disabled = True
                self.valNewPassword.disabled = True
                self.newPassword.hint_text_color_normal = [1, 99/255, 99/255,1]
                self.valNewPassword.hint_text_color_normal = [1, 99/255, 99/255,1]

                self.setpw.disabled = True
    
    def setNewPassword(self):
        
        if len(self.newPassword.text)==0:
            self.newPassword.error =True
            self.newPassword.helper_text=("Can't be empty")
            return
        
        if self.newPassword.text == self.valNewPassword.text:
            print("set Password")
        else:
            self.valNewPassword.error =True
            self.valNewPassword.helper_text=("Passwords are not the same")
            return
        

    def back(self):
        self.clearbeforeleave()
        self.manager.current = 'login'



#Step 1 TFA
class Tfa(Screen):
    def __init__(self, **kwargs):
        super(Tfa, self).__init__(**kwargs)

        self.app = MDApp.get_running_app()

        self.username = ObjectProperty(None)


    def validateText(self):
        self.username.text = str(self.username.text).replace(" ","")

    def sendMail(self):

        if self.app.pm.forgottPassword_Step1(self.username.text):
            self.username.text=""
            self.app.pm.forgottPassword_Step2()
            self.manager.current = 'forgotpassword'
        else:
            self.username.error = True
            self.username.helper_text = ("No User found with this Name")
    
    def back(self):
        self.username.text=""
        self.manager.current = 'login'



class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.inEditMode = False
        self.hasItemSelectet = False
        self.somethingChangedOnCurrentItem = False
        self.listfullyloaded = True

        # LeftPanel
        self.tf_search = ObjectProperty(None)
        # RightPanel
        self.lbPlatformName = ObjectProperty(None)
        self.btEdit = ObjectProperty(None)
        self.btAdd = ObjectProperty(None)
        self.btDelete = ObjectProperty(None)
        self.btDeselect = ObjectProperty(None)

        # MainPanel
        self.btchangePlatformName = ObjectProperty(None)
        self.btchangeimg = ObjectProperty(None)
        self.tf_username = ObjectProperty(None)
        self.tf_password = ObjectProperty(None)
        self.tf_email = ObjectProperty(None)
        self.tf_securitykey = ObjectProperty(None)
        self.tf_phone = ObjectProperty(None)
        self.tf_link = ObjectProperty(None)
        self.show_password = ObjectProperty(None)
        self.show_secKey = ObjectProperty(None)
        # Password Manager
        self.app = MDApp.get_running_app()
        self.enterInit()

    # InternStuff
    def enterInit(self):
        self.generatePasswordPopup = GeneratePasswordPopup_Pop(self.setgeneratedpassword)
        self.fileChooserPopup = FilechooserPopup(self.chooseFileFileChosserPopup, os.path.abspath(os.getcwd()))

        self.listItems = []
        self.listItemsSortName = []
        self.listItemsSortPlatform = []
        self.listItemsDefault = []
        self.sortingtype = ""
        self.currentItem = ListItem
        self.copyToClipBoard= CopyToClipBoard()
        self.whichSavePopup = ""
        self.savewarningbufferitem = None

        self.maxID = 1

        

    # <editor-fold desc="Popups">
    def ChangenamePopup(self, text):

        self.cnp = MDTextField(
            text=text,
            required=True,
            helper_text_mode="on_error",
            helper_text="Enter text",
            foreground_color=(207 / 255, 244 / 255, 210 / 255, 1),
            on_text_validate=self.on_enterChangenamePopup,
            id="textfieldID",
            text_color_focus=(207 / 255, 244 / 255, 210 / 255, 1),
            line_color_focus=(86 / 255, 197 / 255, 150 / 255, 1),
        )

        self.changePlatformNamePopup = Popup(title='Change Name Of Profile',
                                             title_size=25,
                                             content=self.cnp,
                                             separator_color=(86 / 255, 197 / 255, 150 / 255, 1),
                                             size_hint=(None, None),
                                             size=(400, 200)
                                             )
        self.changePlatformNamePopup.open()

    def on_enterChangenamePopup(self, textfield):
        self.changePlatformNamePopup_textfield = textfield
        if textfield.text != "":
            
            self.lbPlatformName.text = textfield.text[0:27]
            textfield.text = ""
            self.changePlatformNamePopup.dismiss()
            if not self.hasItemSelectet:
                self.add_save_changes()
    

    def SaveingWarningPopup(self, which=""):
        self.whichSavePopup = which

        content = BoxLayout(orientation="horizontal", padding=(0, 100, 0, 0), spacing=230)

        content.add_widget(MDRaisedButton(
            md_bg_color=(123 / 255, 228 / 255, 149 / 255, 1),
            pos_hint={'center_x': .4, 'center_y': .6},
            text="Save",
            text_color=(0, 0, 0, 1),
            on_press=self.add_save_changes))

        content.add_widget(MDRaisedButton(
            md_bg_color=(123 / 255, 228 / 255, 149 / 255, 1),
            pos_hint={'center_x': .4, 'center_y': .6},
            text="Discard",
            text_color=(0, 0, 0, 1),
            on_press=self.CloseSaveingWarningPopup))

        self.saveingWarningPopup = Popup(title='        Want to save Changes?',
                                         title_size=25,
                                         content=content,
                                         separator_color=(86 / 255, 197 / 255, 150 / 255, 1),
                                         size_hint=(None, None),
                                         size=(400, 200)
                                         )
        self.saveingWarningPopup.open()

    # this Methode Should always be called to close the popup and reset the states of "self.savewarningbufferitem"
    def CloseSaveingWarningPopup(self, obj=None):
        self.saveingWarningPopup.dismiss()

        if self.whichSavePopup == "":

            if (obj != None):
                if obj.text == "Discard":
                    self.somethingChangedOnCurrentItem = False
                    self.inEditMode = False
                    self.hasItemSelectet = False
                    self.setButtonStates()
                    self.loadIndexFromScrollList(self.savewarningbufferitem)
                else:
                    self.add_save_changes()
                    self.loadIndexFromScrollList(self.savewarningbufferitem)
            else:
                self.add_save_changes()

        else:
            if (obj != None):
                if obj.text == "Discard":
                    self.somethingChangedOnCurrentItem = False
                    self.inEditMode = False
                    self.hasItemSelectet = False
                    self.setButtonStates()
                    self.deselectindex()
                else:
                    self.add_save_changes()
                    self.somethingChangedOnCurrentItem = False
                    self.inEditMode = False
                    self.hasItemSelectet = False
                    self.setButtonStates()
                    self.deselectindex()
            else:
                self.add_save_changes()

    def openGeneratePasswordPopup(self):
        if self.inEditMode or not self.hasItemSelectet:
            self.generatePasswordPopup.open()

    def setgeneratedpassword(self, text):
        self.tf_password.text = str(text)
        self.generatePasswordPopup.dismiss()

    def FileChosserPopup(self):
        self.fileChooserPopup.open()

    def chooseFileFileChosserPopup(self, path):

        if not self.somethingChangedOnCurrentItem:

            if self.hasItemSelectet:
                currentattr = self.currentItem.get(what="IMG")

                if currentattr != path:
                    self.somethingChangedOnCurrentItem = True
                    self.setButtonStates()

        if self.hasItemSelectet:
            self.currentItem.setIMG(path)
            print("UI: IMG Selected on ID:",self.currentItem.get("ID"),"IMG",self.currentItem.get("IMG"))


    def logoutPopup(self):
        print("UI: Opening Logout Popup")

        content = BoxLayout(padding=(0,10,0,0))
        content.add_widget(MDRaisedButton(
            size_hint=(.2,.4),
            text ="Logout",
            md_bg_color=(123/255, 228/255, 149/255, 1),
            text_color=(0,0,0,1),
            on_press=self.continueLogout
        ))
        content.add_widget(BoxLayout(
            size_hint=(.6,.4)

        ))
        content.add_widget(MDRaisedButton(
            size_hint=(.2,.4),
            text ="Cancle",
            md_bg_color=(123/255, 228/255, 149/255, 1),
            text_color=(0,0,0,1),
            on_press=self.closeLoginPopup
        ))

        self.LogoutPopup = Popup(title='Logout?',
                                            title_size=25,
                                            content=content,
                                            separator_color=(86 / 255, 197 / 255, 150 / 255, 1),
                                            size_hint=(None, None),
                                            size=(400, 200)
                                            )
        self.LogoutPopup.open()
    
    def closeLoginPopup(self,Obj=None):
        print("UI: Canceling Logout")
        self.LogoutPopup.dismiss()



    # </editor-fold>

    #Event Runs once When Entering Main Page. Runs before Kv is Loaded
    def on_enter(self):
        print('UI: Creating main Page from Profile')
        self.enterInit()
        self.ids.container.data = []
        self.loadListOfItems()


    #ButtonEvent When pressing logount
    def logout(self):
        self.logoutPopup()
 
    # After Lopgout Popup This will Called when Pressing on Logout in the Popup
    def continueLogout(self,obj=None):
        print("UI: Logout User")
        self.LogoutPopup.dismiss()
        self.app.pm.logout()
        self.ids.container.clear_widgets()
        self.hasItemSelectet = False
        self.inEditMode = False
        self.setButtonStates()
        self.manager.current = 'login'


    # CSV:  ID;PlatformName;Username;Password;Email;SecurityKey;Telephon;Link;ImgPath
    #This Function loads all Entries in CSV to the list on the left
    #Calls addToListInUi()
    def loadListOfItems(self):
        loadlist = self.app.pm.getAllPasswords()
        self.maxID = len(loadlist.index)
        self.ids.container.clear_widgets()
        counter = 1

        for index, row in loadlist[1:].iterrows():
            newlistItem = ListItem()

            newlistItem.setid_(counter)
            newlistItem.setPlatformName(self.app.pm.translate(row["PlatformName"]))
            newlistItem.setUserName(self.app.pm.translate(row["Username"]))
            newlistItem.setPassword(self.app.pm.translate(row["Password"]))
            newlistItem.setEmail(self.app.pm.translate(row["Email"]))
            newlistItem.setSecurityKey(self.app.pm.translate(row["SecurityKey"]))
            newlistItem.setPhoneNr(self.app.pm.translate(row["Telephon"]))
            newlistItem.setLink(self.app.pm.translate(row["Link"]))
            newlistItem.setIMG(self.app.pm.translate(row["ImgPath"]))

            newlistItem.listref = self

            counter = counter+1

            self.addToListInUi(newlistItem)

        if self.sortingtype == "NAME":
            self.sortingNames()
        if self.sortingtype == "PLATFORM":
            self.sortingPlatform()

    #Adds Item to list to the left
    def addToListInUi(self, widget):
        self.listItems.append(widget)
        self.ids.container.add_widget(widget)
    
    #Event when Presed the Copy Button under the Textfields
    def copyTextFromFieldToClipboard(self,textfield):
        self.copyToClipBoard.copy(textfield.text)
    
    #Always Updates the Search bar for All Passwords on Text Input
    def search(self):
        self.tf_search.text = str(self.tf_search.text).replace(" ", "")

        if (self.tf_search.text != ""):
            self.listfullyloaded = False
            self.ids.container.clear_widgets()
            for widget in self.listItems:
                if (str(self.tf_search.text).lower() in str(widget.get("PLATFORMNAME")).lower()
                        or str(self.tf_search.text).lower() in str(widget.get("USERNAME")).lower()
                        or str(self.tf_search.text).lower() in str(widget.get("EMAIL")).lower()):
                    self.ids.container.add_widget(widget)
        elif not self.listfullyloaded:
            self.listfullyloaded = True
            self.ids.container.clear_widgets()
            for widget in self.listItems:
                self.ids.container.add_widget(widget)
    #Sorting Mode Name
    def sortingNames(self):
        self.tf_search.text = ""
        self.sortingtype = "NAMES"
        self.listItemsSortName = sorted(self.listItems, key=lambda x: x.platformName.lower())
        self.ids.container.clear_widgets()
        for widget in self.listItemsSortName:
            self.ids.container.add_widget(widget)
        print("UI: Sorting Names")
    #Sorting Mode Platform
    def sortingPlatform(self):
        self.tf_search.text = ""
        self.sortingtype = "PLATFORM"
        self.listItemsSortPlatform = sorted(self.listItems, key=lambda x: os.path.basename(
            x.get("IMG")).lower())
        self.ids.container.clear_widgets()
        for widget in self.listItemsSortPlatform:
            self.ids.container.add_widget(widget)
        print("UI: Sorting Platform")
    #Sorting Mode Logo/Img Name
    def sortingDefault(self):
        self.tf_search.text = ""
        self.sortingtype = ""
        self.listItemsDefault = self.listItems
        self.ids.container.clear_widgets()
        for widget in self.listItemsDefault:
            self.ids.container.add_widget(widget)
        print("UI: Sorting Default")

    # Get item from list on the left when filled
    def loadIndexFromScrollList(self, item):

        # if nothing Changed or nothing is selected Load Item
        if not self.somethingChangedOnCurrentItem or not self.hasItemSelectet:
            self.savewarningbufferitem = None
            self.currentItem = item
            print("UI: Loading Index From List",self.currentItem.get("ID"))

            self.inEditMode = False
            self.hasItemSelectet = True
            self.setButtonStates()

            # MainPanel
            self.lbPlatformName.text = str(self.currentItem.platformName)
            self.tf_username.text = str(self.currentItem.userName)
            self.tf_password.text = str(self.currentItem.password)
            self.tf_email.text = str(self.currentItem.email)
            self.tf_securitykey.text = str(self.currentItem.securityKey)
            self.tf_phone.text = str(self.currentItem.phone)
            self.tf_link.text = str(self.currentItem.link)

        # Forgot to save Popup start
        else:
            self.savewarningbufferitem = item
            self.SaveingWarningPopup()

    # <editor-fold desc="Right Panel Buttons">

    #Start Edit Mode
    def editSelectedIndex(self):
        print("UI: EditMode")
        if self.btEdit.state == "normal":
            self.inEditMode = False
        else:
            self.inEditMode = True
        self.setButtonStates()

    #Gets Called when New Password Entry is made or You press on Save after Changin something
    def add_save_changes(self, obj=None):
        the_new_widget = ListItem()
        if obj != None:
            self.CloseSaveingWarningPopup()

        # Save Button is Active
        # If Item is Selected Save current Profile
        if self.hasItemSelectet:
            print("UI: start Saving")
            # Save Process: Everything Variable inside ListItem should bes aved
            self.currentItem.setPlatformName(self.lbPlatformName.text)
            self.currentItem.setUserName(self.tf_username.text)
            self.currentItem.setPassword(self.tf_password.text)
            self.currentItem.setEmail(self.tf_email.text)
            self.currentItem.setSecurityKey(self.tf_securitykey.text)
            self.currentItem.setPhoneNr(self.tf_phone.text)
            self.currentItem.setLink(self.tf_link.text)

            self.app.pm.edit_password(
                _id=self.currentItem.get(what="ID"),
                platform=self.currentItem.get(what="PLATFORMNAME"),
                userName=self.currentItem.get(what="USERNAME"),
                Password=self.currentItem.get(what="PASSWORD"),
                eMail=self.currentItem.get(what="EMAIL"),
                securityKey=self.currentItem.get(what="SECURITYKEY"),
                telephon=self.currentItem.get(what="PHONE"),
                link=self.currentItem.get(what="LINK"),
                imgPath=self.currentItem.get(what="IMG")
            )

            if self.sortingtype == "NAME":
                self.sortingNames()
            if self.sortingtype == "PLATFORM":
                self.sortingPlatform()
            if self.sortingtype=="":
                self.sortingDefault()

            self.somethingChangedOnCurrentItem = False
            self.setButtonStates()

        # Add Button is Active
        # If nothing is Selected and Profile name is not Empty Add Profile
        else:
            if self.lbPlatformName.text != "":
                print("UI: add new profile")
                the_new_widget.platformName = self.lbPlatformName.text
                the_new_widget.listref = self
                the_new_widget.setPlatformName(self.lbPlatformName.text)
                the_new_widget.setUserName(self.tf_username.text)
                the_new_widget.setPassword(self.tf_password.text)
                the_new_widget.setEmail(self.tf_email.text)
                the_new_widget.setSecurityKey(self.tf_securitykey.text)
                the_new_widget.setid_(str(self.maxID))
                self.maxID = self.maxID + 1
                self.addToListInUi(the_new_widget)

                self.app.pm.add_password(
                    the_new_widget.get(what="PLATFORMNAME"),
                    userName=the_new_widget.get(what="USERNAME"),
                    Password=the_new_widget.get(what="PASSWORD"),
                    eMail=the_new_widget.get(what="EMAIL"),
                    securityKey=the_new_widget.get(what="SECURITYKEY"),
                    telephon=the_new_widget.get(what="PHONE"),
                    link=the_new_widget.get(what="LINK"),
                    imgPath=the_new_widget.get(what="IMG")
                )

                self.loadIndexFromScrollList(the_new_widget)

                if self.sortingtype == "NAME":
                    self.sortingNames()
                if self.sortingtype == "PLATFORM":
                    self.sortingPlatform()
                if self.sortingtype == "":
                    self.sortingDefault()


            else:
                print("UI: Enter a Title!")
                self.ChangenamePopup("")

    #Deletes Selected Entry from List and CSV
    def deleteindex(self):
        print("UI: Delet Index:", self.currentItem.get("ID"))
        if self.currentItem in self.listItems:
            self.app.pm.delete_password(self.currentItem.get("ID"))

            for item in self.listItems:
                if(item == self.currentItem):
                    self.listItems.remove(item)
            self.maxID = self.maxID-1
            #self.listItems = []
            #self.loadListOfItems()

            if self.sortingtype == "NAME":
                self.sortingNames()
            if self.sortingtype == "PLATFORM":
                self.sortingPlatform()
            if self.sortingtype=="":
                self.sortingDefault()

            self.hasItemSelectet = False
            self.inEditMode = False
            self.setButtonStates()


        else:
            print("UI: Nothing selected")
    
    #Deselects Current selection
    def deselectindex(self):
        if not self.somethingChangedOnCurrentItem:
            self.hasItemSelectet = False
            self.inEditMode = False
            self.somethingChangedOnCurrentItem = False
            self.setButtonStates()

        else:
            self.SaveingWarningPopup(which="deselect")
            print("UI: Save loss warning Popup")

    # </editor-fold>

    #Change Screen
    def changeScreen(self):
        if self.manager.current == 'login':
            self.manager.current = 'mainscreen'
        else:
            self.manager.current = 'login'

    # Set States of Button and TextFields based on self.hasItemSelectet and self.inEditMode and self.somethingChangedOnCurrentItem
    def setButtonStates(self):

        # If Item is Selected Deactivate Everything
        if self.hasItemSelectet:
            # RightPanel
            self.btAdd.text = "Save"

            # Logic to only Activate Save button on Change of something
            if self.somethingChangedOnCurrentItem:
                self.btAdd.disabled = False
            else:
                self.btAdd.disabled = True

            self.btEdit.disabled = False
            self.btDelete.disabled = False
            self.btDeselect.disabled = False

            # If Item is Selected But EditMode is active, Activate Everything in MainPanel
            if self.inEditMode:

                # MainPanel
                self.btchangePlatformName.disabled = False
                self.btchangeimg.disabled = False
                self.tf_username.disabled = False
                self.tf_password.disabled = False
                self.tf_email.disabled = False
                self.tf_securitykey.disabled = False
                self.tf_phone.disabled = False
                self.tf_link.disabled = False

                self.tf_password.password = False
                self.tf_securitykey.password = False
                self.show_password.disabled = True
                self.show_secKey.disabled = True

            # If Item is Selected but EditMode is Deactivated Disable Everything in MainPanel
            else:
                # RightPanel
                self.btEdit.state = "normal"

                # MainPanel
                self.btchangePlatformName.disabled = True
                self.btchangeimg.disabled = True
                self.tf_username.disabled = True
                self.tf_password.disabled = True
                self.tf_email.disabled = True
                self.tf_securitykey.disabled = True
                self.tf_phone.disabled = True
                self.tf_link.disabled = True

                self.tf_password.password = True
                self.tf_securitykey.password = True
                self.show_password.disabled = False
                self.show_secKey.disabled = False

        # If Nothing is Selected Reset Everything
        else:
            self.inEditMode = False

            # RightPanel
            self.btAdd.text = "Add"
            self.btAdd.disabled = False
            self.btEdit.state = "normal"
            self.btEdit.disabled = True
            self.btDelete.disabled = True
            self.btDeselect.disabled = True

            # MainPanel
            self.lbPlatformName.text = ""
            self.btchangePlatformName.disabled = False
            self.btchangeimg.disabled = True
            self.tf_username.disabled = False
            self.tf_password.disabled = False
            self.tf_email.disabled = False
            self.tf_securitykey.disabled = False
            self.tf_phone.disabled = False
            self.tf_link.disabled = False

            self.tf_username.text = ""
            self.tf_password.text = ""
            self.tf_email.text = ""
            self.tf_securitykey.text = ""
            self.tf_phone.text = ""
            self.tf_link.text = ""

    # <editor-fold desc="Main Panel Scoll View Editable stuff">

    #When Pressed on add or The Pen Icon to Create a Name for a new Profile or change the Existing one
    def changPlatformName(self):
        if not self.hasItemSelectet:
            if self.lbPlatformName.text == "":
                self.ChangenamePopup("")
            else:
                self.ChangenamePopup(self.lbPlatformName.text)
        else:
            if self.inEditMode:
                self.ChangenamePopup(self.lbPlatformName.text)

    #Change Image path of selected Item
    def changeImagePath(self):
        if self.hasItemSelectet:
            self.FileChosserPopup()
    #Unhide Passwords when Holding down on the Eye-off Icon
    def showTextField(self, obj):
        obj.password = False
    #Hide Textfields when released
    def hideTextField(self, obj):
        obj.password = True

    #Looks for Changes in the Textfields and sets the self.somethingChangedOnCurrentItem flag when something changes to activate Save function
    def onTextfieldText_Change(self, obj, what):
        # If False check on a change
        if not self.somethingChangedOnCurrentItem:

            if self.hasItemSelectet:
                currentattr = getattr(self.currentItem, what)

                if currentattr != obj.text:
                    self.somethingChangedOnCurrentItem = True
                    self.setButtonStates()

    def generatePassword(self):
        self.GeneratePasswordPopup()

    # </editor-fold>


####################################################################################
class Manager(ScreenManager):
    login = ObjectProperty(None)
    mainscreen = ObjectProperty(None)
    register = ObjectProperty(None)
    forgotpassword = ObjectProperty(None)
    tfa = ObjectProperty(None)


class ScreensApp(MDApp):
    def build(self):
        self.pm = Passwort_Manager()
        self.icon = "Logo_512x512.png"
        Window.shape_color_key = (0, 0, 0, 1)
        self.title = 'Prime Manager'
        self.theme_cls.theme_style = "Dark"
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()
