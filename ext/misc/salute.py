from structure import extensions
import sys
class NatsumePersonaGreets(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "salute"
        self.alias = [self.name]
        self.isSystem = True
        self.alias = [self.name]
        self.args = [
            {
                "name": "phrase",
                "optional": True
            }
        ]
        self.run = self.execute

    def execute(self, phrase):
        currPersona = self.base.currMod["personality"].currPersona
        if "list" == phrase:
            sys.stdout.write("{}Available Salutes: {}\n".format(self.utils.BLUE, self.utils.CLR))
            for persona in currPersona.keys():
                sys.stdout.write("{}<{:^10}> [natsume] {} {}\n".format(
                    self.utils.XRED, persona, currPersona[persona], self.utils.CLR))
        elif phrase in currPersona:
            sys.stdout.write("{}[{}] {}{}\n".format(
                    self.utils.XRED, 
                    "Natsume",
                    self.base.currMod["personality"].currPersona[phrase],
                    self.utils.CLR
                    ))
        else:
            if phrase: self.utils.printError("salute", "{} isn't registered!".format(phrase))


