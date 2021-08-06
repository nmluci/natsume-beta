from structure import extensions

class NatsumeOwner(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "owner"
        self.__Ver = "1.0"
        self.alias = [self.name]

    def execute(self):
        print("Current Loaded Modules")
        print("Non-Critical")
        for mod in self.base.currMod:
            if not self.base.currMod[mod].isSystem: print(self.base.currMod[mod].name)

        print("\nCritical")
        for mod in self.base.currMod:
            if self.base.currMod[mod].isSystem: print(self.base.currMod[mod].name)