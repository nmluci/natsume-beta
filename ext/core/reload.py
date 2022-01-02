from typing import final
from structure import extensions

class NatsumeExtReload(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "reload"
        self.isSystem = True
        self.alias = ['r', "reload"]
        self.args = [
            {
                "name": "modules",
                "default": ""
            }
        ]

    def execute(self, modules):
        if modules in self.base.currMod:
            try:
                self.base.ExtLoader.reload(modules)
            except Exception as e:
                self.utils.printError("Reload", e)
            else:
                print("Ext. {} Reloaded!".format(modules))
        elif "all" == modules.lower():
            self.base.ExtLoader.reloadAll()
        elif "config" == modules.lower():
            self.base.settings = self.utils.getConfig()
            self.base.ExtLoader.reloadAll(self.base.settings["natsume"]["extensions"])
        else:
            self.utils.printError("Reload", "{} isn't a valid module...".format(modules))