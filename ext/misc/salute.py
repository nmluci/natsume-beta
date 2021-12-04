from structure import extensions
import sys
class NatsumePersonaGreets(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "salute"
        self.alias = [self.name]
        self.isSystem = True
        self.alias = [self.name]
        self.run = self.execute

    def execute(self, args):
        if type(args) == list and len(args) != 0: 
            args = args[0]
        else:
            print("ops")
            return -1
        if "list" == args:
            ctr = 1
            sys.stdout.write("{}Available Salutes: {}\n".format(self.utils.BLUE, self.utils.CLR))
            for persona in self.base.currMod["personality"].currPersona.keys():
                sys.stdout.write("{}[{}] {} {}\n".format(self.utils.XRED, ctr, persona, self.utils.CLR))
                ctr += 1
        elif args in self.base.currMod["personality"].currPersona:
            sys.stdout.write("{}[{}] {}{}\n".format(
                    self.utils.XRED, 
                    "Natsume",
                    self.base.currMod["personality"].currPersona[args],
                    self.utils.CLR
                    ))
        else:
            self.utils.printError("salute", "{} isn't registered!".format(args))


