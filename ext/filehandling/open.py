from structure import extensions
from pathlib import Path
import json

class NatsumeFileOpen(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "openfile"
        self.desc = "open a file and save it in memory"
        self.alias = ["open"]
        self.args = [
            {
                "name": "file",
                "type": Path,
                "desc": "relative path to file"
            },
            {
                "name": "env",
                "type": str,
                "desc": "variable name to store",
                "default": "cache",
                "optional": True
            },
            {
                "name": "filetype",
                "type": str,
                "desc": "file parsed as",
                "optional": True,
                "default": "text"
            }
        ]

    def execute(self, file, env, filetype):
        if filetype == "json":
            data = json.loads(open(file, "r", encoding='UTF-8').read())
        elif filetype == "text":
            data = open(file, "r", encoding='UTF-8').read()
        else:
            self.utils.printError("openfile", "this feature not yet implemented")
            return
        
        self.base.cache[env] = {
            "data": data,
            "form": env
        }
        print(json.dumps(self.base.cache, indent=3))
