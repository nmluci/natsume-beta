import os
import json

class NatsumeUtils:
    def __init__(self):
        self.__VER = 1.0
        
    class SigHandler:
        def __init__(self):
            self.__VER = 1.0
    
        def graceExit(self, handler=None, frame=None):
            print("Exiting...")
            exit()

        def graceNoticed(self, handler=None, frame=None):
            print("Exiting...?")
            exit()

    class ConfigLoader:
        def __init__(self, configType=None):
            self.type = configType
            self.dConfig = dict()

            if (self.type):
                self.configPath = os.path.join("structure", "config", "{}.json".format(self.type))
                self.defConfigPath = os.path.join("structure", "defaultConfig", "{}.json".format(self.type))
            
        def __iterConfigFiles(self, modules):
            moduleList = list()
            for nModule in modules:    
                for root, subdir, files in os.walk(os.path.join(nModule)):
                    for file in files:
                        moduleList.append([root, file])
            return moduleList

        def init(self):
            with open(os.path.join("structure", "config", "base.json"), "r+") as f:
                self.dConfig = json.load(f)

        def __setDefault(self) -> dict:
            with open(self.defConfigPath) as f:
                self.dConfig[self.type] = json.load(f)
            self.save()

        def loadAll(self) -> dict:
            moduleList = self.__iterConfigFiles(self.moduleMap.keys())

            for module in moduleList:
                with open(os.path.join(module[0], module[1]), "r+") as f:
                    moduleNoExt = module[1].split(".")[0]

                    if moduleNoExt in self.extensionMap.keys():
                        moduleNoExt = self.extensionMap[moduleNoExt]
                        
                        if moduleNoExt in self.dConfig.keys():
                            self.dConfig[moduleNoExt] += json.load(f)
                        else:
                            self.dConfig[moduleNoExt] = json.load(f)

            return self.dConfig

        def load(self) -> dict:
            if not self.type: 
                print("NO MODULE!")
                return {"fuee": "NULL"}

            if os.path.exists(self.configPath) and os.stat(self.configPath).st_size != 0:
                with open(self.configPath) as config:
                    self.dConfig[self.type] = json.load(config)
                return self.dConfig
            
        def save(self):
            with open(self.configPath, "w+") as fp:
                json.dump(self.dConfig[self.type], fp, indent=3)
        
        def reload(self, obj: dict) -> dict:
            self.dConfig = obj
            obj[self.type] = self.load()
            return obj