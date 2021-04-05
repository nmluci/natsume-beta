from colorama import Fore, init
from structure import extensions
import sys, os

class NatsumeAbout(extensions.NatsumeExt):
    def __init__(self):
        super().__init__()
        self.name = "about"
        self.desc = "Help Function"
        self.alias = ["h"]
    
    def execute(self, main, args):
        print("Natsume-chan")
        for ext in main.currMod:
            main.currMod[ext].help(main)
        print("By Cxizaki <{}winterspiritze{}@outlook.com{}>".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.RESET))