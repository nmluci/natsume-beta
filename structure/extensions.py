import importlib, os, sys, inspect
from . import utils as utils

class NatsumeExtMan:
    def __init__(self, moduleList: list = []):
        self.__VER = 1.0
        self.utils = utils.NatsumeUtils()
        self.__moduleList = moduleList
        self.__loadedExt = 0
        self.__extFolder = "ext"
        self.__extList = dict()

    def getCurrentModules(self):
        print(self.__extList)
        if self.__loadedExt == 0:
            self.utils.printError("ExtLoader", "No Modules Has Been Loaded!")
            exit()
        currMod = list()
        for moduleKey in self.__extList: currMod.append(moduleKey)
        return currMod
    
    def loadAll(self):
        if self.__loadedExt != 0:
            self.printError("ExtLoader", "Modules Is Already Loaded!")
            exit()

        extRef = dict()
        for module in self.__moduleList:
            for submodule in os.listdir(os.path.join(self.__extFolder, module)):
                if ("__" in submodule) or (".py" not in submodule): continue

                submodule = submodule.split(".")[0]
                fullModule = "{}.{}.{}".format(self.__extFolder, module, submodule)
                tempModule = importlib.import_module(fullModule, "{}.{}".format(self.__extFolder, module))
                moduleName = inspect.getmembers(tempModule, inspect.isclass)[0][0]
                extRef[submodule] = getattr(tempModule, moduleName)()
                # print(submodule, moduleName)
                if fullModule in sys.modules:
                    self.__loadedExt += 1
                else:
                    self.printError("ExtLoader", "{} Module Failed To Load!".format(fullModule))

            self.__extList[submodule] = tempModule
        return extRef

class NatsumeExt:
    def __init__(self):
        self.__VER = 1.0
        self.name = "NatsumeDefault"
        self.desc = str()
        self.args = dict()
        self.utils = utils.NatsumeUtils()
        self.isSystem = False
        self.help = str()

    def execute(self, main, args):
        pass