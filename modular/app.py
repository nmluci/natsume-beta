import importlib
import os
import sys
import inspect

libDir = "ext"
fynModuleList = ['persona', 'admin']
currModules = dict()

for module in fynModuleList:
    tempModules = dict()
    for submodule in os.listdir(os.path.join("ext", module)):
        if "__" in submodule: continue
        submodule = submodule.split(".")[0]
        fullModule = "ext.{}.{}".format(module, submodule)
        tempModules[submodule] = importlib.import_module(fullModule, "ext.{}".format(module))
        moduleName = inspect.getmembers(tempModules[submodule], inspect.isclass)[0][0]
        tempModules[submodule] = getattr(tempModules[submodule], moduleName)()
        print(fullModule in sys.modules.keys())   

    currModules[module] = tempModules
# for lib in fynLoad:
#     print(lib)
#     lib.execute()
for moduleKey in currModules.keys():
    for submoduleKey in currModules[moduleKey].keys():
        print(submoduleKey)
        currModules[moduleKey][submoduleKey].execute()
