from typing import final
from structure import extensions

class NatsumeExtReload(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "reload"
        self.isSystem = True
        self.alias = [self.name]
        self.args = [
            {
                "name": "modules"
            }
        ]

    def execute(self, args):
        if args[0] in self.base.currMod:
            try:
                self.base.ExtLoader.reload(args[0])
            except OSError as e:
                self.utils.printError("Reload", e)
            else:
                print("Ext. {} Reloaded!".format(args[0]))
        elif "all" == args[0].lower():
            self.base.ExtLoader.reloadAll()
        elif "config" == args[0].lower():
            self.base.settings = self.utils.getConfig()
            self.base.ExtLoader.reloadAll(self.base.settings["natsume"]["extensions"])
        else:
            self.utils.printError("Reload", "{} isn't a valid module...".format(args))