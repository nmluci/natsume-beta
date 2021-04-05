import os
import json

class NatsumeUtils:
    def __init__(self):
        self.__VER = 1.0

    class SigHandler:
        def __init__(self):
            self.__VER = 1.0

        def graceExit(self, handler=None, frame=None):
            print('Exiting...')
            exit()
        
        def graceNotice(self, handler=None, frame=None):
            print("Exiting...?")
            exit()

    class ConfigLoader:
        def __init__(self, configType=None):
            self.type = configType
            self.dConfig = dict()

            if self.type:
                self.configPath = os.path.join("structure", "config", "{}.json".format(self.type))
                self.defConfigPath = os.path.join("structure", "defaultConfig", "{}.json".format(self.type))

        def __setDefault(self):
            with open(self.defConfigPath) as f:
                self.dConfig[self.type] = json.load()
            self.save()
        
        def load(self):
            if os.path.exists(self.configPath) and os.stat(self.configPath).st_size != 0:
                    with open(self.ConfigPath) as config:
                        self.dConfig[self.type] = json.load(config)
            else:
                print("No Config...")
                self.__setDefault()

        def save(self):
            with open(self.configPath, "w+") as fp:
                json.dump(self.dConfig[self.type], fp, indent=3)

        def reload(self, obj: dict) -> dict:
            self.dConfig = obj
            obj[self.type] = self.load()
            return obj

    class NatsumeExtLoader:
        def __init__(self, extension: str):
            self.extName = extension
            self.__VER = 1.0

        def __iterExtFiles(self):
            moduleList = list()
            