import os, signal
from colorama import init, Fore

class NatsumeUtils:
    def __init__(self):
        self.__VER = 1.0
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
    
    def printError(self, mod, err):
        print("{}[{}] {}{}".format(self.RED, mod, err, self.CLR))