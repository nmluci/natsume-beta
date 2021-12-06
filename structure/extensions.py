from __future__ import annotations

from types import ModuleType
from typing import List, Dict
from dataclasses import dataclass
from pathlib import Path
import importlib, sys, inspect

from . import utils

@dataclass
class ExtObj:
    classObj  : NatsumeExt = None
    moduleObj : ModuleType = None
    alias     : str = None

    @classmethod
    def validateArgs(cls, obj: NatsumeExt):
        printError = utils.NatsumeUtils().printError
        printInfo  = utils.NatsumeUtils().printInfo

        if obj.args is None:
            printError("ValidateArgs", f"Skipping {obj.name}: No Args found!")
            return
        if type(obj.args) != list: 
            printError("ValidateArgs", "Invalid type!")
            obj.args = [{}]
        
        for arg in obj.args:
            if "name" not in arg.keys():
                printInfo("VaildateArgs", "Args Name isn\'t listed!")
            if "optional" not in arg.keys():
                arg["optional"] = False
            if "type" not in arg.keys():
                arg["type"] = str
            if "default" not in arg.keys():
                arg["default"] = ""

class NatsumeExtMan:
    def __init__(self, main, utility: utils.NatsumeUtils, moduleList: List = []):
        self.__VER = 1.0
        self.__loadedExt = 0
        self.__extFolder = "ext"
        self.utils: utils.NatsumeUtils = utility
        self.settings = self.utils.getConfig()
        self.moduleList = self.settings["natsume"]["extensions"]
        self.modules : Dict[str, ExtObj] = dict()
        self.extRef  : Dict[str, ExtObj.classObj] = dict() 
        self.base = main

    def execute(self, ext, args):
        try:
            ext : ExtObj.classObj = self.extRef[ext]
            minimumArgs : List[Dict] = list(arg for arg in ext.args if not arg["optional"]) if ext.args else None
            
            # No Argument needed
            if minimumArgs == None:
                self.utils.printInfo("Execute", "No argument detected")
                args = None
            else:
                for seq, arg in enumerate(minimumArgs):
                    attempt = 1
                    if arg["name"] in args:
                        continue
                    if f'args_{seq+1}' in args:
                        args[arg['name']] = args[f'args_{seq+1}']
                        args.pop(f'args_{seq+1}')  
                        continue

                    for i in range(3):
                        temp = input(f"{arg['name']}: ")
                        if not temp and attempt <= 3: 
                            if arg["optional"]: 
                                temp = arg.get('default', None)
                                break
                            elif attempt != 3:
                                attempt += 1
                                continue
                            else:
                                raise ValueError(f"{arg['name']} can't be empty")
                        
                        if "cancel" in temp.lower(): 
                            raise Exception("Action canceled")

                        args[arg['name']] = temp
                        break
                                    
        except Exception as e:
            self.utils.printError("Execute", f"{e}")
        except KeyError:
            self.utils.printError("Execute", f"{ext} isn't a valid alias")
        except ValueError as e:
            self.utils.printError("Execute", f"{e}")
        else:
            if args:
                ext.run(**args)
            else:
                ext.run()

    def getCurrentModules(self, alias: str=None):
        if self.__loadedExt:
            self.utils.printError("getCurrentModules", "No modules has been loaded!")
            exit()
        if alias:
            return self.extRef[alias]
        return self.modules.items()

    def reload(self, mod):
        try:
            newExtRef = self.extRef.copy()
            newExtObj = self.modules.copy()

            for ext, extObj in self.modules.items():
                if mod in extObj.alias:
                    newModule = importlib.reload(extObj.moduleObj)

                    for mod in inspect.getmembers(newModule, inspect.isclass):
                        if issubclass(mod[1], NatsumeExt):
                            self.utils.printInfo("ExtReload", f"Reloaded {mod[1]}")
                            classObj = mod[1](utils=self.utils, main=self.base)
                            moduleName = classObj.name
                            if moduleName != extObj.classObj.name:
                                self.utils.printInfo("ExtReload", f"Module's name has changed: {ext.classObj.name}->{moduleName}")
                    
                    newAlias = list(filter(lambda x: x not in extObj.alias, classObj.alias))
                    self.utils.printInfo("ExtReload", "Removing old instance from list")
                    newExtObj.pop(extObj.classObj.name)
                    self.utils.printInfo("ExtReload", "Removing aliases from list")
                    for alias in extObj.alias:
                        newExtRef.pop(alias)

                    ExtObj.validateArgs(classObj)
                    newExtObj[moduleName] = ExtObj(classObj, newModule, classObj.alias)
                    
                    for alias in classObj.alias:
                        if alias == "NatsumeBaseExtensions": continue
                        if alias not in newExtRef.keys():
                            newExtRef[alias] = newExtObj[moduleName].classObj
                            if alias in newAlias: self.utils.printInfo("ExtReload", f"Found new alias: {alias}")
                        else:
                            self.utils.printInfo("ExtReload", newExtObj[moduleName].classObj.alias)
                            self.utils.printInfo("ExtReload", extObj.classObj.alias)
                            raise AttributeError(f"Conflicting Aliases Found! {alias}")

        except Exception as e:
            self.utils.printError("ExtLoader", e)
        else:
            self.modules = newExtObj
            self.extRef = newExtRef
            self.base.currMod = self.extRef

    def loadAll(self):
        if self.__loadedExt != 0:
            self.utils.printError("ExtLoader", "Modules already loaded!")
        
        try:
            for module in self.moduleList:
                for submodule in filter(lambda x: ("__" not in x.name) and (".py" == x.suffix), 
                                        list(Path(self.__extFolder, module).glob("*"))):
                    
                    pkgName = f"{self.__extFolder}.{module}"
                    fullModule = str(submodule).replace("\\", ".").split(".py")[0]
                    moduleObj = importlib.import_module(fullModule, pkgName)
                    
                    for mod in inspect.getmembers(moduleObj, inspect.isclass):
                        if issubclass(mod[1], NatsumeExt):
                            self.utils.printInfo("ExtLoader", f"Found {mod[1]}")
                            classObj = mod[1](utils=self.utils, main=self.base)
                            moduleName = classObj.name
                        else:
                            self.utils.printError("ExtLoader", F"Found {mod[1]}")
                    
                    if not (classObj or fullModule in sys.modules):
                        raise AttributeError(f"{module} contains no suitable extensions")
                    # Mapping aliases and generic name into classObj
                    ExtObj.validateArgs(classObj)
                    self.modules[moduleName] = ExtObj(classObj, moduleObj, classObj.alias)
                    
                    for alias in self.modules[moduleName].classObj.alias:
                        if alias == "NatsumeBaseExtensions": continue
                        if alias not in self.extRef.keys():
                            self.extRef[alias] = self.modules[moduleName].classObj
                        else:
                            raise AttributeError(f"Conflicting Aliases Found! {alias}")

                    self.utils.printInfo("ExtLoader", f"{moduleName}, {fullModule}")

        except Exception as e:
            self.utils.printError("ExtLoader", e)
        finally:
            for cmd, mod in self.extRef.items():
                self.utils.printInfo("Available Cmdlet", f"{cmd} {mod}")
            return self.extRef

    def reloadAll(self):
        self.__loadedExt = 0
        newExtDict: Dict[str, ExtObj] = dict()
        newExtRef: Dict[str, ExtObj.classObj] = dict()

        try:
            for mod, ext in self.modules.items():
                moduleObj = importlib.reload(ext.moduleObj)

                for mod in inspect.getmembers(moduleObj, inspect.isclass):
                    if issubclass(mod[1], NatsumeExt):
                        self.utils.printInfo("ExtReload", f"Found {mod[1]}")
                        classObj = mod[1](utils=self.utils, main=self.base)
                        moduleName = classObj.name
                        if moduleName != ext.classObj.name:
                            self.utils.printInfo("ExtReload", f"Module's name has changed: {ext.classObj.name}->{moduleName}")


                ExtObj.validateArgs(classObj)
                newAlias = list(filter(lambda x: x not in ext.alias, classObj.alias))
                newExtDict[moduleName] = ExtObj(classObj, moduleObj, classObj.alias)

                    
                for alias in classObj.alias:
                    if alias == "NatsumeBaseExtensions": continue
                    if alias not in newExtRef.keys():
                        newExtRef[alias] = newExtDict[moduleName].classObj
                        if alias in newAlias: self.utils.printInfo("ExtReload", f"Found new alias: {alias}")
                    else:
                        self.utils.printInfo("ExtReload", newExtDict[moduleName].classObj.alias)
                        self.utils.printInfo("ExtReload", ext.classObj.alias)
                        raise AttributeError(f"Conflicting Aliases Found! {alias}")
                
                self.utils.printInfo("ExtReload", f"Reloaded {moduleName}")
        except Exception as e:
            self.utils.printError("ExtReload", e)
        else:
            self.modules = newExtDict
            self.extRef = newExtRef
            self.base.currMod = self.extRef

class NatsumeExt:
    aliasBind = dict()
    def __init__(self, main, utils=utils.NatsumeUtils()):
        self.__VER = 1.0
        self.base = main
        self.utils = utils
        self.name = "NatsumeBaseExtensions"
        self.args : list[dict] = None
        self.help =  "Wha! Nothing to see here!"
        self.group = "Misc"
        self.desc = self.help
        self.alias = [self.name]
        self.isSystem = False
        self.run = self.execute

    def execute(self, args):
        return print("Whoa, Unimplemented Feature Here! Nice nice.... now.. GET BACK TO WORK!")

        