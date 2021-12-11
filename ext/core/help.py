from structure import extensions
import sys, os

class NatsumeHelp(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Help"
        self.alias = ["h", "help", "?"]
        self.desc = "Shows Help"
        self.help = "This is HELP!"
        self.args = [
            {
                "name": "name",
                "desc": "Command name",
                "default": None,
                "optional": True
            }

        ]
        self.run = self.execute

    def execute(self, name):
        if not name:
            for _, ext in self.base.ExtLoader.getCurrentModules():
                self.parseCommandInfo(ext.classObj)
        else:
            self.parseCommandInfo(self.base.ExtLoader.getCurrentModules(name))

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

        