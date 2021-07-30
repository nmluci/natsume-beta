from structure import extensions
import os

class NatsumeExtClearScreen(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "cls"
        self.desc = "Well... Clear Screen... Digitally"
        self.help = self.desc
        self.alias = [self.name]

    def execute(self, args):
        os.system("cls")        