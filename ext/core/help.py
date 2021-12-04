from structure import extensions
import sys, os

class NatsumeHelp(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Help"
        self.alias = ["h", "help"]
        self.desc = "Shows Help"
        self.help = "This is HELP!"
        self.args = [
            {
                "name": "name",
                "desc": "Command name",
                "optional": True
            }

        ]
        self.run = self.altExc

    def execute(self, cmdlets):
        if cmdlets:
            self.parseCommandInfo(self.base.ExtLoader.getModule(cmdlets))
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
        if not args:
            for name, ext in self.base.ExtLoader.getCurrentModules():
                self.parseCommandInfo(ext.classObj)
        else:
            self.parseCommandInfo(self.base.ExtLoader.getCurrentModules(args[0]))
    def parseArgsInfo(self, cmdlet:extensions.ExtObj):
        if not cmdlet.args:
            return None
        else:
            argList = list()
            for cmd in cmdlet.args:
                argList += [f"{self.utils.XRED if not cmd['optional'] else self.utils.BLUE}{cmd['name']}{self.utils.CLR}"]

            return ", ".join(argList)

    def parseCommandInfo(self, cmdlet: extensions.ExtObj.classObj):
        sys.stdout.write("{:>3}<{}>{}\n".format(
            self.utils.XBLUE, cmdlet.name, self.utils.CLR
        ))
        sys.stdout.write("{:>6}Aliases: {}{}{}\n".format(
            self.utils.BLUE, self.utils.RED, ", ".join(cmdlet.alias), self.utils.CLR 
        ))
        sys.stdout.write("{:>6}Description: {}{}{}\n".format(
            self.utils.BLUE, self.utils.RED, cmdlet.desc, self.utils.CLR 
        ))
        sys.stdout.write("{:>6}Args: {}{}{}\n".format(
            self.utils.BLUE, self.utils.RED, self.parseArgsInfo(cmdlet), self.utils.CLR 
        ))

        