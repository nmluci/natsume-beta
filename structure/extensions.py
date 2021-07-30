from __future__ import annotations

from types import ModuleType
from typing import List, Dict
from dataclasses import dataclass
from pathlib import Path
import importlib, sys, inspect

from . import utils


# modules
# Extension's Name: ExtObj

@dataclass
class ExtObj:
    classObj  : NatsumeExt = None
    moduleObj : ModuleType = None
    alias     : str = None

class NatsumeExtMan:
    def __init__(self, main, moduleList: List = []):
        self.__VER = 1.0
        self.__loadedExt = 0
        self.__extFolder = "ext"
        self.utils = utils.NatsumeUtils()
        self.moduleList = moduleList
        self.modules : Dict[str, ExtObj] = dict()
        self.extRef  : Dict[str, ExtObj.classObj] = dict() # Alias, Class
        self.base = main

    def getCurrentModules(self):
        if self.__loadedExt:
            self.utils.printError("getCurrentModules", "No modules has been loaded!")
            exit()

        return  list(obj.name for _, obj in self.modules)
    
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
                            classObj = mod[1](main=self.base)
                            moduleName = classObj.name
                            if moduleName != extObj.classObj.name:
                                self.utils.printInfo("ExtReload", f"Module's name has changed: {ext.classObj.name}->{moduleName}")
                    
                    newAlias = list(filter(lambda x: x not in extObj.alias, classObj.alias))
                    self.utils.printInfo("ExtReload", "Removing old instance from list")
                    newExtObj.pop(extObj.classObj.name)
                    self.utils.printInfo("ExtReload", "Removing aliases from list")
                    for alias in extObj.alias:
                        newExtRef.pop(alias)

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
            import traceback
            traceback.print_exc()
            self.utils.printError("ExtLoader", e)
        else:
            self.modules = newExtObj
            self.extRef = newExtRef
            return self.extRef  

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
                            classObj = mod[1](main=self.base)
                            moduleName = classObj.name
                        else:
                            self.utils.printError("ExtLoader", F"Found {mod[1]}")
                    
                    if not (classObj or fullModule in sys.modules):
                        raise AttributeError(f"{module} contains no suitable extensions")
                    # Mapping aliases and generic name into classObj
                    self.modules[moduleName] = ExtObj(classObj, moduleObj, classObj.alias)
                    
                    for alias in self.modules[moduleName].classObj.alias:
                        if alias == "NatsumeBaseExtensions": continue
                        if alias not in self.extRef.keys():
                            self.extRef[alias] = self.modules[moduleName].classObj
                        else:
                            raise AttributeError(f"Conflicting Aliases Found! {alias}")

                    self.utils.printInfo("ExtLoader", f"{moduleName}, {fullModule}")

        except Exception as e:
            import traceback
            traceback.print_exc()
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
                        classObj = mod[1](main=self.base)
                        moduleName = classObj.name
                        if moduleName != ext.classObj.name:
                            self.utils.printInfo("ExtReload", f"Module's name has changed: {ext.classObj.name}->{moduleName}")

                                    
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
            import traceback
            traceback.print_exc()
            self.utils.printError("ExtReload", e)
        else:
            self.modules = newExtDict
            self.extRef = newExtRef
            return self.extRef 

class NatsumeExt:
    def __init__(self, main):
        self.__VER = 1.0
        self.base = main
        self.utils = utils.NatsumeUtils()
        self.name = "NatsumeBaseExtensions"
        self.args = dict()
        self.help =  "Wha! Nothing to see here!"
        self.desc = self.help
        self.alias = [self.name]
        self.isSystem = False
    
    def execute(self, args):
        return print("Whoa, Unimplemented Feature Here! Nice nice.... now.. GET BACK TO WORK!")
