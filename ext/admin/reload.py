from os import error
from typing import final
from structure import extensions

class NatsumeExtReload(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "reload"
        self.isSystem = True

    def execute(self, args):
        try:
            self.base.ExtLoader.reload(args)
        except error as e:
            self.utils.printError("Reload", e)
        else:
            print("Ext. {} Reloaded!".format(args[0]))