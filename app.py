from structure import utils
from structure import extensions
class NatsumeApp:
    def __init__(self):
        self.VER = 0.3
        self.isExit = False
        self.currMod = dict()
        self.currCmd = ""
        self.utils = utils.NatsumeUtils()
        self.settings = self.utils.getConfig()
        self.debug = self.settings["natsume"]["debug"]
        self.ExtLoader = extensions.NatsumeExtMan(self, self.settings["natsume"]["extensions"])
        self.currMod = self.ExtLoader.loadAll()
        self.currMod['salute'].execute("startup")

    def argParser(self, args: str):
        try:
            if args == "": return self.utils.printError("app", "What's your command?")
            args = self.utils.argsParser(args)
            self.ExtLoader.execute(args[0], args[1:])
        except Exception as e:
            self.utils.printError("Main", e)
            
    def main(self):
        isExit = False
        while (not isExit):
            self.argParser(str(input("natsume > ")))
        
if __name__ == "__main__":
    app = NatsumeApp()
    app.main()