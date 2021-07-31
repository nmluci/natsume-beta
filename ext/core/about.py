from colorama import Fore, init, Style
from structure import extensions
import sys, os, psutil

class NatsumeAbout(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "about"
        self.desc = "Help Function"
        self.alias = ["about", "whoami", "me"]

    def execute(self, args):
        self.process = psutil.Process(os.getpid())
        sys.stdout.write("{}Natsume-chan <version {}>{}\n".format(
            Fore.LIGHTMAGENTA_EX, self.base.VER, Style.RESET_ALL
        ))
        sys.stdout.write("{}Python Version: {}{}.{}{}\n".format(
            Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, 
            sys.version_info.major, sys.version_info.minor, Style.RESET_ALL
        ))
        sys.stdout.write("{}Memory Usage: {}{:.2f} MB {}\n".format(
            Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, self.process.memory_info().rss/2**20, Style.RESET_ALL
        ))
        sys.stdout.write("{}Uptime: {}{}{}\n".format(
            Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, self.base.utils.getUptime(), Style.RESET_ALL
        ))
        sys.stdout.write("{}Uptime (Since last reload): {}{}{}\n".format(
            Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, self.utils.getUptime(), Style.RESET_ALL
        ))
        sys.stdout.write("{}Available Commands: {}{}{}\n".format(
            Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, len(self.base.ExtLoader.modules), Style.RESET_ALL
        ))
        # for ext in self.base.currMod:
        #     print(ext, self.base.currMod[ext].help)

        print("By Cxizaki <{}winterspiritze{}@outlook.com{}>".format(Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.RESET))