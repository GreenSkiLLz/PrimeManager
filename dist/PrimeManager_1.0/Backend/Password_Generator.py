import string
import random
class Password_Generator():
    def __init__(self):
        self.letters_lower = list(string.ascii_lowercase)
        self.letters_upper= list(string.ascii_uppercase)
        self.digits =list(string.digits)
        self.punctuation = list("!#$%()*+,-./:;=?@[]^_{|}~")
        self.pickerlist = []

    def generatePassword(self,slide_chars,cb_upperlower,cb_numbers,cb_symbols):
        self.pickerlist = []

        self.pickerlist.extend(self.letters_lower)
        if cb_upperlower:
            self.pickerlist.extend(self.letters_upper)
        if cb_numbers:
            self.pickerlist.extend(self.digits)
        if cb_symbols:
            self.pickerlist.extend(self.punctuation)

        random.shuffle(self.pickerlist)
        gen=""
        gen=gen.join(random.choices(self.pickerlist,k=slide_chars))
        return gen

