from structure import extensions

class NatsumeOwner(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.__Name = "owner"
        self.__Ver = "1.0"

    def execute(self, args):
        print("Current Module: {}".format(self.__Name))