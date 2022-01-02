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
        print(env)
        if len(self.base.cache) == 0:
            return self.utils.printInfo("showdata", "empty!")

        if env == 'all':
            print(json.dumps(self.base.cache, indent=3))
        else:        
            datatype = self.base.cache[env]["form"]
            data = self.base.cache[env]["data"]

            if datatype == "json":
                return print(json.dumps(data, indent=3))
            elif datatype == "text":
                return print(f"{env}: {data}")