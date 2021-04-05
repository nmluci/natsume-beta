from structure import extensions
import sys
class NatsumePersonaGreets(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "greet"
        self.isSystem = True

    def execute(self, args):
        if type(args) == list: args = args[0]
        if args in self.base.currMod["persona"].currPersona:
            sys.stdout.write("{}{}{}\n".format(
                    self.utils.XRED, 
                    self.base.currMod["persona"].currPersona[args],
                    self.utils.CLR
                    ))


