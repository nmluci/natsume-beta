from structure import extensions
import os

class NatsumeExtClearScreen(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cls"
        self.desc = "Well... Clear Screen... Digitally"
        self.help = self.desc
        self.alias = [self.name]

    def execute(self):
        os.system("cls")        