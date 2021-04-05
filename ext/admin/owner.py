from structure import extensions

class NatsumeOwner(extensions.NatsumeExt):
    def __init__(self):
        super().__init__()
        self.__Name = "owner"
        self.__Ver = "1.0"

    def execute(self, main):
        print("Current Module: {}".format(self.__Name))