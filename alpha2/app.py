from structure import utils as nUtils
from structure import argsParser as nParser
import sys
import signal

class NatsumeApp:
    def __init__(self):
        self.Utils = nUtils.NatsumeUtils()
        self.isExit = False
        self.currCmd = ""
        self.__natsumeCfg = self.Utils.ConfigLoader().init()
        self.Parser = nParser.NatsumeParser()

        signal.signal(signal.SIGINT, self.Utils.SigHandler.graceNoticed)
        print("Arguments Passed: {} [{} items]".format(" ".join(sys.argv[1:]), len(sys.argv)-1))

    def getInput(self):
        stats = 0
        while (stats != -1):
            rawCmd = str(input("Natsume > "))
            self.Parser.parse(rawCmd)
        if stats == -1:
            print("Welp dats short.")
            exit()

if __name__ == "__main__":
    app = NatsumeApp()
    app.getInput()