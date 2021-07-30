from structure import utils
from structure import extensions

class NatsumeApp:
    def __init__(self):
        self.__VER = 0.3
        self.isExit = False
        self.currMod = dict()
        self.currCmd = ""
        self.utils = utils.NatsumeUtils()
        self.settings = self.utils.getConfig()
        self.ExtLoader = extensions.NatsumeExtMan(self, self.settings["natsume"]["extensions"])
        self.currMod = self.ExtLoader.loadAll()
        self.currMod['salute'].execute(["startup"])

    def argParser(self, args: str):
        if args == "": return self.utils.printError("app", "What's your command?")
        args = self.utils.argsParser(args)
        if args[0] in self.currMod:
            self.currMod[args[0]].execute(args[1:])
        else:
            self.utils.printError("app", "{} not found!".format(args[0] if len(args) >= 1 else "Command"))
        
    def main(self):
        isExit = False
        while (not isExit):
            self.argParser(str(input("natsume > ")))
        
if __name__ == "__main__":
    app = NatsumeApp()
    app.main()