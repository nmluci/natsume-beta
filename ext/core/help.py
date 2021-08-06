from structure import extensions
import sys, os

class NatsumeHelp(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "Help"
        self.alias = ["h", "help"]
        self.desc = "Shows Help"
        self.help = "This is HELP!"
        self.args = [
            {
                "name": "cmdlets",
                "default": "",
                "optional": True 
            }
        ]

    def execute(self, cmdlets):
        if cmdlets:
            self.parseCommandInfo(self.base.ExtLoader.getModule(cmdlets))
        else:
            for name, ext in self.base.ExtLoader.getCurrentModules():
                self.parseCommandInfo(ext)

    def parseArgsInfo(self, cmdlet:extensions.ExtObj):
        return (", ".join(list(x["name"] for x in cmdlet.classObj.args))) if cmdlet.classObj.args else None

    def parseCommandInfo(self, cmdlet: extensions.ExtObj):
        if cmdlet.classObj.isSystem:
            if not self.base.debug: return
            sys.stdout.write("{:>3}<System> {}{}\n".format(
                self.utils.XRED, self.utils.XBLUE, cmdlet.classObj.name, self.utils.CLR
            ))
        else:
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

        