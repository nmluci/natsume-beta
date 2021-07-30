import os, signal, json, traceback, re
from typing import List
from colorama import init, Fore

class NatsumeUtils:
    __VER = "0.3b"
    def __init__(self):
        init(convert=True)
        self.RED = Fore.MAGENTA
        self.GREEN = Fore.GREEN
        self.BLUE = Fore.BLUE
        self.XRED = Fore.LIGHTMAGENTA_EX
        self.XGREEN = Fore.LIGHTGREEN_EX
        self.XBLUE = Fore.LIGHTBLUE_EX
        self.CLR = Fore.RESET
        signal.signal(signal.SIGINT, self.graceExit)
        signal.signal(signal.SIGTERM, self.graceExit)

    def graceExit(self, handler=None, frame=None):
        print("Exiting...")
        exit()
    
    def getConfig(self, submodule=None) -> dict:
        try:
            with open("profile.json", "r+") as cfg:
                config = json.load(cfg)
            return config
        except FileNotFoundError:
            self.printInfo("ConfigLoader", "Existing Configuration is not existed!")
            defaultProfile = {
                "natsume": {
                    "persona": "maid",
                    "extensions": [
                        "core",
                        "misc"
                    ]
                }
            }

            with open("profile.json", "w") as f:
                f.write(json.dumps(defaultProfile, indent=3))
            return defaultProfile

    def reloadConfig(self) -> dict:
        with open("profile.json", "r+") as cfg:
            return json.load(cfg)

    def printError(self, mod, err):
        print("{}[{}] {}{}".format(self.RED, mod, err, self.CLR))

    def printInfo(self, mod, info):
        print(f"{self.BLUE}[{mod}] {info}{self.CLR}")

    def argsParser(self, args: str) -> List[str]:
        return re.findall("(?:\".*?[^\\\\]\"|\S)+", args)

    def isDigit(self, args: str) -> bool:
        try:
            int(args)
        except ValueError:
            return False
        else:
            return True
