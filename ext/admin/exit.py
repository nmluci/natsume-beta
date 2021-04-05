from structure import extensions

class NatsumeExit(extensions.NatsumeExt):
    def __init__(self):
        super().__init__()
        self.__VER = 1.0
        self.isSystem = True

    def execute(self, main, args):
        exit()
        