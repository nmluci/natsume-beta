from structure import extensions
import sys, os, psutil

class NatsumeAbout(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "about"
        self.desc = "Help Function"
        self.alias = ["about", "whoami", "me"]

    def execute(self):
        self.process = psutil.Process(os.getpid())
        sys.stdout.write("{}Natsume-chan <version {}>{}\n".format(
            self.utils.XRED, self.base.VER, self.utils.CLR
        ))
        sys.stdout.write("{}Python Version: {}{}.{}{}\n".format(
            self.utils.XRED, self.utils.XCYAN, 
            sys.version_info.major, sys.version_info.minor, self.utils.CLR
        ))
        sys.stdout.write("{}Memory Usage: {}{:.2f} MB {}\n".format(
            self.utils.XRED, self.utils.XCYAN, self.process.memory_info().rss/2**20, self.utils.CLR
        ))
        sys.stdout.write("{}Uptime: {}{}{}\n".format(
            self.utils.XRED, self.utils.XCYAN, self.base.utils.getUptime(), self.utils.CLR
        ))
        sys.stdout.write("{}Uptime (Since last reload): {}{}{}\n".format(
            self.utils.XRED, self.utils.XCYAN, self.utils.getUptime(), self.utils.CLR
        ))
        sys.stdout.write("{}Available Commands: {}{}{}\n".format(
            self.utils.XRED, self.utils.XCYAN, len(self.base.ExtLoader.modules), self.utils.CLR
        ))
        sys.stdout.write("{}Debugging Status: {}{}{}\n".format(
            self.utils.XRED, self.utils.XCYAN, self.base.debug, self.utils.CLR
        ))
        # for ext in self.base.currMod:
        #     print(ext, self.base.currMod[ext].help)

        print("By Cxizaki <{}winterspiritze{}@outlook.com{}>".format(self.utils.XRED, self.utils.XCYAN, self.utils.CLR))