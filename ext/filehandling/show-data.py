from structure import extensions
from pathlib import Path
import json

class NatsumeFileShowdata(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "showdata"
        self.desc = "show all data stored in memory"
        self.alias = ["showdata"]
        self.args = [
            {
                "name": "env",
                "type": str,
                "desc": "variable name to store",
                "default": "all"
            }
        ]

    def execute(self, env):
        if len(self.base.cache) == 0:
            return self.utils.printInfo("showdata", "empty!")


        if env == 'all':
            for key in self.base.cache.keys():
                print(key)
                if self.base.cache[key]["form"] == "json":
                    return print(json.dumps(self.base.cache[key]["data"], indent=3))
                elif self.base.cache[key]["form"] == "text":
                    return print(f"{env}: {self.base.cache[key]['data']}")
                elif self.base.cache[key]["form"] == "mangaBackup":
                    print(f"manga count: {len(self.base.cache[key]['data']['manga'])}")
                    print(f"doujin count: {len(self.base.cache[key]['data']['doujin'])}")
                    return
        else:        
            if env not in self.base.cache.keys():
                return self.utils.printInfo("showdata", f"{env} not existed")

            datatype = self.base.cache[env]["form"]
            data = self.base.cache[env]["data"]

            if datatype == "json":
                return print(json.dumps(data, indent=3))
            elif datatype == "text":
                return print(f"{env}: {data}")