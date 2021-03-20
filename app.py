from structure import utils as nUtils
import sys
import signal

class NatsumeApp:
    def __init__(self):
        self.Utils = nUtils.NatsumeUtils()
        self.isExit = False
        self.currCmd = ""
        self._natsumeCfg = ""
        self.Utils.ConfigLoader().loadAll()
        signal.signal(signal.SIGINT, self.Utils.SigHandler.graceNoticed)
        print("Arguments Passed: {} [{} items]".format(" ".join(sys.argv[1:]), len(sys.argv)-1))

    def getInput(self):
        stats = 0
        while (stats != -1):
            rawCmd = str(input("Natsume > "))
            stats = self.Utils.ArgsParser(rawCmd)
        if stats == -1:
            print("Welp dats short.")
            exit()

if __name__ == "__main__":
    app = NatsumeApp()
    app.getInput()