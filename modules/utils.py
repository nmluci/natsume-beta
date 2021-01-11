from typing import Optional
import colorama
import sys
import os
import signal
import argparse

class NatsumeUtils:
    def __init__(self):
        colorama.init()
        
        self.CRED = colorama.Fore.RED
        self.CCYAN = colorama.Fore.CYAN
        self.CMAGENTA = colorama.Fore.MAGENTA
        self.CXMAGENTA = colorama.Fore.LIGHTMAGENTA_EX
        self.CRESET = colorama.Style.RESET_ALL
        self.VER = '1.0'
        self.isExiting = False

        signal.signal(signal.SIGINT, self.graceExit)
        signal.signal(signal.SIGTERM, self.graceExit)

    def graceExit(self, sigterm=None, frame=None):
        self.printInfo("Exiting...")
        self.isExiting = not self.isExiting
        if self.isExiting: exit()

    def getOpt(self, opt: list):
        self.printInfo('Module to Choose', ", ".join(opt))
        return self.printInfo("Choosen", self.getInfo("Option"))

    def cls(self):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        # sys.stdout.write("{}NatsumeAI Utility v{}{}\n".format(self.CCYAN, self.VER, self.CRESET))

    # print informational
    def printInfo(self, msg, opt=None):
        sys.stdout.write("{}{}{}{}\n".format(self.CXMAGENTA, msg, ": " + self.CCYAN + opt if opt is not None else "", self.CRESET))
        if opt is not None: return opt

    def printError(self, err):
        sys.stdout.write("{}[ERR] {}{}\n".format(self.CRED, err, self.CRESET))
    
    def getInfo(self, msg):
        sys.stdout.write("{}{}{}: ".format(self.CMAGENTA, msg, self.CRESET))
        var = input()
        self.cls()
        self.cls()
        # print("\n")
        return var

    def argsParser(self):
        arg = argparse.ArgumentParser(
            prog="cxtools",
            exit_on_error=False
        )
        
        subParser = arg.add_subparsers(dest='submodule')
        helpParse = subParser.add_parser('help', help='show help menu')
        
        # Done
        redditParse = subParser.add_parser("reddit", help='Reddit submodule')
        redditParse.add_argument('subreddit', type=str, help="subreddit name")
        redditParse.add_argument('-n', type=int, help='number of posts', default=25)
        redditParse.add_argument('-i', help='inclusive download', action="store_true")

        # Barely
        nhentaiParse = subParser.add_parser("nhentai", help='nHentai submodule')
        nhentaiParse.add_argument('sauce', type=int, help='get info about the sauce', nargs="*")
        
        # Should be Sufficient
        imgurParse = subParser.add_parser("imgur", help='Imgur submodule')
        imgurParse.add_argument("url", type=str, help='Imgur URL', nargs="*")
        
        # Barely
        pornhubParse = subParser.add_parser("ph", help='PH submodule')
        pornhubParse.add_argument("url", type=str, help="PH URL", nargs="*")
        
        return arg.parse_args()

    def helpInfo(self, cmd=None):
        if cmd is None:
            self.printInfo("Help", "NOTHING!")
    