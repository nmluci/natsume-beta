from os import pardir
from structure import utils, extensions
import re
class NatsumeApp:
    def __init__(self):
        self.__VER = 0.3
        self.isExit = False
        self.currMod = dict()
        self.currCmd = ""
        self.Utils = utils.NatsumeUtils()
        self.ExtLoader = extensions.NatsumeExtMan(["admin"])
        # self.ExtLoader = extensions.NatsumeExtMan()
        self.currMod = self.ExtLoader.loadAll()

    def argParser(self, args: str):

        args = re.findall("(?:\".*?[^\\\\]\"|\S)+", args)
        if args[0] in self.currMod:
            self.currMod[args[0]].execute(self, args[1:])
        else:
            self.Utils.printError("app", "{} not found!".format(args[0] if len(args) >= 1 else "Command"))
        # if len(args.split(" ")) >= 2 and args.split(" ")[0] in self.currMod:
        #     parsed = args.split("\"")
        #     temp = []
        #     print(parsed)
            
        #     for cmd in parsed:
        #         if ("" in cmd.split(" ")): 
        #             temp.append(cmd.split(" ")[0])
        #         else:
        #             temp.append(cmd)
        #     print(temp)
        # elif args in self.currMod:
        #         self.currMod[args].execute(self)
        # else:
        #     self.Utils.printError("app", "{} not found!".format(args if len(args) >= 1 else "Command"))

    def main(self):
        isExit = False
        while (not isExit):
            self.argParser(str(input("natsume > ")))
        
if __name__ == "__main__":
    app = NatsumeApp()
    app.main()