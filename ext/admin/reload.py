from os import error
from typing import final
from structure import extensions

class NatsumeExtReload(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "reload"
        self.isSystem = True

    def execute(self, args):
        if args[0] in self.base.currMod:
            try:
                self.base.ExtLoader.reload(args)
            except error as e:
                self.utils.printError("Reload", e)
            else:
                print("Ext. {} Reloaded!".format(args[0]))
        elif "config" == args[0].lower():
            self.base.settings = self.utils.getConfig()
            self.base.ExtLoader.reloadAll(self.base.settings["natsume"]["extensions"])
        else:
            self.utils.printError("Reload", "{} isn't loaded...".format(args))