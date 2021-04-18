import importlib, os, sys, inspect
from . import utils as utils

class NatsumeExtMan:
    def __init__(self, main, moduleList: list = []):
        self.__VER = 1.0
        self.utils = utils.NatsumeUtils()
        self.__moduleList = moduleList
        self.__moduleMap = dict()
        self.__loadedExt = 0
        self.__extFolder = "ext"
        self.__extList = dict()
        self.base = main

    def getCurrentModules(self):
        print(self.__extList)
        if self.__loadedExt == 0:
            self.utils.printError("ExtLoader", "No Modules Has Been Loaded!")
            exit()
        currMod = list()
        for moduleKey in self.__extList: currMod.append(moduleKey) 
        return currMod
    
    def reload(self, ext):
        ext = ext[0]
        if ext not in self.base.currMod: return self.utils.printError("ExtLoader", "Ext. {} Cannot Be Found!".format(ext))
        newModule = importlib.reload(self.__moduleMap[ext])
        newName = inspect.getmembers(newModule, inspect.isclass)[0][0]
        self.base.currMod[ext] = getattr(newModule, newName)(self.base)

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
                self.__moduleMap[submodule] = importlib.import_module(fullModule, "{}.{}".format(self.__extFolder, module))
                moduleName = inspect.getmembers(self.__moduleMap[submodule], inspect.isclass)[0][0]
                extRef[submodule] = getattr(self.__moduleMap[submodule], moduleName)(self.base)

                if fullModule in sys.modules:
                    self.__loadedExt += 1
                else:
                    self.printError("ExtLoader", "{} Module Failed To Load!".format(fullModule))
                self.__extList[submodule] = self.__moduleMap[submodule]
        return extRef

class NatsumeExt:
    def __init__(self, main):
        self.__VER = 1.0
        self.base = main
        self.utils = utils.NatsumeUtils()
        self.name = "Natsume Base Extension"
        self.args = dict()
        self.help = "Wha! Nothing to see here!"
        self.desc = self.help
        self.isSystem = False

    def execute(self, args):
        print("Whoa, Unimplemented Feature! Nice nice... now.. GET BACK TO WORK!")