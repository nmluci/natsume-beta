from structure import extensions
import sys, os

class NatsumeHelp(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Help"
        self.alias = ["h", "help"]
        self.desc = "Shows Help"
        self.help = "This is HELP!"
        self.args = {
            "cmdlets": {
                "desc": "Command name",
                "optional": True
            }
        }
        self.run = self.altExc

    def beta_execute(self, args):
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

    def execute(self, args):
        self.altExc(args) if "alt" in args else self.beta_execute(args)

    def altExc(self, args):
        for name, ext in self.base.ExtLoader.getCurrentModules():
            self.parseCommandInfo(ext)

    def parseArgsInfo(self, cmdlet:extensions.ExtObj):
        return ", ".join(list(x for x in cmdlet.classObj.args))

    def parseCommandInfo(self, cmdlet: extensions.ExtObj):
        sys.stdout.write("{:>3}<{}>{}\n".format(
            self.utils.XBLUE, cmdlet.classObj.name, self.utils.CLR
        ))
        sys.stdout.write("{:>6}Aliases: {}{}{}\n".format(
            self.utils.BLUE, self.utils.RED, ", ".join(cmdlet.alias), self.utils.CLR 
        ))
        sys.stdout.write("{:>6}Description: {}{}{}\n".format(
            self.utils.BLUE, self.utils.RED, cmdlet.classObj.desc, self.utils.CLR 
        ))
        sys.stdout.write("{:>6}Args: {}{}{}\n".format(
            self.utils.BLUE, self.utils.RED, self.parseArgsInfo(cmdlet), self.utils.CLR 
        ))
        