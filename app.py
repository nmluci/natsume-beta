from inspect import Traceback
from structure import utils, extensions, database
class NatsumeApp:
    def __init__(self, debug=False):
        self.VER = 0.3
        self.debug = debug
        self.isExit = False
        self.currMod = dict()
        self.currCmd = ""
        self.cache = dict()
        self.utils = utils.NatsumeUtils()
        self.database = database.NatsumeDatabase()
        self.ExtLoader = extensions.NatsumeExtMan(self, self.utils, self.database)
        self.currMod = self.ExtLoader.loadAll()
        self.currMod['salute'].execute("startup")
        
    def argParser(self, args: str):
        try:
            if args == "": return self.utils.printError("app", "What's your command?")
            cmdlet, argMap = self.utils.argsParser(args)
            self.ExtLoader.execute(cmdlet, argMap)
        except Exception as e:
            self.utils.printError("Main", e)
            
    def main(self):
        isExit = False
        if self.debug:
            self.database.create_db()

        while (not isExit):
            self.argParser(str(input("natsume > ")))
        
if __name__ == "__main__":
    import sys
    app = NatsumeApp("--debug" in sys.argv)
    if "--colorless" in sys.argv:
        sys.stdout.write("[ConfigLoader] Executing in B/W Mode...\n")
    app.main()