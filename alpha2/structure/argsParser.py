from . import utils as nUtils

class NatsumeParser:
    def __init__(self):
        self.__natsumeCmd = nUtils.NatsumeUtils().ConfigLoader("extra").load()
        self.Utils = nUtils.NatsumeUtils()
        self.__availableCmd = self.__getAvailableCmdlet()
        self.__VER = 1.0

    def __getAvailableCmdlet(self) -> list:
        cmdlets = list()
        for cmdlet in self.__natsumeCmd["command"]:
            cmdlets.append(cmdlet["commandName"])
        return cmdlets

    def parse(self, args: str):
        argsParsed = args.split(" ")

        if len(argsParsed) == 1:
            if argsParsed[0] in self.__availableCmd:
                self.run(argsParsed[0])
        else:
            for arg in argsParsed:
                if arg in self.__availableCmd:
                    self.run(arg)

    def run(self, cmd: str):
        if cmd == "exit":
            self.Utils.SigHandler().graceExit()
        elif cmd == "help":
            for cmdlet in self.__natsumeCmd["command"]:
                print("{}: {}".format(cmdlet["commandName"], cmdlet["desc"]))
        elif cmd == "loadAll":
            self.Utils.ConfigLoader().loadAll()