from structure import extensions
import sys, os

class NatsumeHelp(extensions.NatsumeExt):
    def __init__(self):
        super().__init__()
        self.__VER = 1.0
        self.name = "about"
        self.desc = "Shows Help"
        self.help = "This is HELP!"
        self.args = {
            "cmdlets": "Command Name"
        }
    def execute(self, main, args):
        sys.stdout.write("Natsume-chan Help Board!\n\n")

        if len(args) >= 1:
            for mods in args:
                if mods in main.currMod:
                    sys.stdout.write("{}<{}>{}\n".format(self.utils.XRED, mods, self.utils.CLR))
                    if main.currMod[mods].help == "": main.currMod[mods].help = "No Info!"
                    sys.stdout.write("\t\"{}\"\n\n".format(main.currMod[mods].help))
        else:
            for mods in main.currMod:
                if main.currMod[mods].isSystem: continue
                sys.stdout.write("<{}>\n".format(mods))
                if main.currMod[mods].desc: sys.stdout.write("\t\"{}\"\n".format(main.currMod[mods].desc))
            sys.stdout.write("Type {}\"help <command here>\"{} to get details information about the command!\n\n"
                                .format(self.utils.XRED, self.utils.CLR))
