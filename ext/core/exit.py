from structure import extensions

class NatsumeExit(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "exit"
        self.__VER = 1.0
        self.isSystem = True
        self.alias = [self.name]
    def execute(self, args):
        self.base.currMod["salute"].execute(["shutdown"])
        exit()
        