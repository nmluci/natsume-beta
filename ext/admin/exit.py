from structure import extensions

class NatsumeExit(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.__VER = 1.0
        self.isSystem = True

    def execute(self, args):
        self.base.currMod["salute"].execute("shutdown")
        exit()
        