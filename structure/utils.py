import colorama
import sys
import signal
import argparse
import random
import re

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
        self.printInfo("\nExiting...")
        self.isExiting = not self.isExiting
        exit()

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
    def verifyOpt(self, msg: str, opt: list = None) -> str:
        if (opt != None):
            parsedOpt = "/".join(opt)
            print("{}{}{}\nOption: {}".format(self.CCYAN, msg, self.CXMAGENTA, parsedOpt))
            resp = str(input("{}Input: {}".format(self.CCYAN, self.CRESET)))
            if ((resp not in opt) or ("" not in resp)): 
                self.printError("Invalid Option!")
                self.verifyOpt(msg, opt)
        else:
            print("{}{}{}".format(self.CCYAN, msg, self.CXMAGENTA))
            resp = str(input("{}Input: {}".format(self.CCYAN, self.CRESET)))
        return resp

    # PEP 295
    def stripIndent(self, s):
        pattern = re.compile(r'^[ \t]*(?=\S)', re.MULTILINE)
        indent = min(len(spaces) for spaces in pattern.findall(s))

        if not indent:
            return s

        return re.sub(re.compile(r'^[ \t]{%s}' % indent, re.MULTILINE), '', s)  
    
    def argsParser(self):
        arg = argparse.ArgumentParser(
            prog="cxtools"
        )
        
        subParser = arg.add_subparsers(dest='submodule')
        helpParse = subParser.add_parser('help', help='show help menu')
        
        # Done
        redditParse = subParser.add_parser("reddit", help='Reddit submodule')
        redditParse.add_argument('subreddit', type=str, help="subreddit name", nargs="+")
        redditParse.add_argument('-n', type=int, help='number of posts', default=25)
        redditParse.add_argument('-i', help='inclusive download', action="store_true")

        # Done
        nhentaiParse = subParser.add_parser("nhentai", help='nHentai submodule')
        nhentaiParse.add_argument('sauce', type=str, help='get info about the sauce', nargs="*")
        nhentaiParse.add_argument('-dl', help='download this sauce', action='store_true')
        nhentaiParse.add_argument('-s', help='search by title', action='store_true')
        nhentaiParse.add_argument('-st', help='search by tags', action='store_true')
        nhentaiParse.add_argument('-l', help='list results', action='store_true')
        nhentaiParse.add_argument('--rand', help='get random hentai', action='store_true')
        
        # Should be Sufficient
        imgurParse = subParser.add_parser("imgur", help='Imgur submodule')
        imgurParse.add_argument("url", type=str, help='Imgur URL', nargs="*")
        
        # Barely
        pornhubParse = subParser.add_parser("ph", help='PH submodule')
        pornhubParse.add_argument("url", type=str, help="PH URL", nargs="*")
        
        animeParse = subParser.add_parser("anime", help="Anime by AniList.co submodule")
        animeParse.add_argument('metaAnime', type=str, help='get info about anime', nargs="*")

        mangaParse = subParser.add_parser("manga", help='Manga by AniList.co submodule')
        mangaParse.add_argument('metaManga', type=str, help='get info about manga', nargs="*")

        return arg.parse_args()

    def helpInfo(self, cmd=None):
        if cmd is None:
            self.printInfo("Help", "NOTHING!")
    
    def getrand(self, range):
        return random.randrange(0, range)