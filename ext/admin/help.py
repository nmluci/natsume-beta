from structure import extensions
import sys, os

class NatsumeHelp(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.__VER = 1.0
        self.name = "about"
        self.desc = "Shows Help"
        self.help = "This is HELP!"
        self.args = {
            "cmdlets": "Command Name"
        }

    def execute(self, args):
        sys.stdout.write("Natsume-chan Help Board!\n\n")

        if len(args) >= 1:
            for mods in args:
                if mods in self.base.currMod:
                    sys.stdout.write("{}<{}>{}\n".format(self.utils.XRED, mods, self.utils.CLR))
                    if self.base.currMod[mods].help == "": self.base.currMod[mods].help = "No Info!"
                    sys.stdout.write("\t\"{}\"\n\n".format(self.base.currMod[mods].help))
        else:
            for mods in self.base.currMod:
                if self.base.currMod[mods].isSystem: continue
                sys.stdout.write("<{}>\n".format(mods))
                if self.base.currMod[mods].desc: sys.stdout.write("\t\"{}\"\n".format(self.base.currMod[mods].desc))
            sys.stdout.write("Type {}\"help <command here>\"{} to get details information about the command!\n\n"
                                .format(self.utils.XRED, self.utils.CLR))
