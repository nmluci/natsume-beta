from colorama import Fore, init
from structure import extensions
import sys, os

class NatsumeAbout(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "about"
        self.desc = "Help Function"
        self.alias = ["about", "whoami", "me"]
    
    def execute(self, args):
        print("Natsume-chan")
        for ext in self.base.currMod:
            print(ext, self.base.currMod[ext].help)

        print("By Cxizaki <{}winterspiritze{}@outlook.com{}>".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.RESET))