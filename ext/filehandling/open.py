import betterproto
from structure import extensions
from ext.filehandling.ext.tachiyomi.compiled import TachiyomiBackup

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
        elif filetype == "manga_backup":
            bp = TachiyomiBackup.Backup()
            
            data = bp.FromString(open(file, "rb").read())
            data = {
                "doujin": list(x for x in filter(lambda x: x.source == 3122156392225024195, data.backup_manga)),
                "manga": list(x for x in filter(lambda x: x.source != 3122156392225024195, data.backup_manga))
            }
            env = "mangaBackup"
        else:
            self.utils.printError("openfile", "this feature not yet implemented")
            return
        
        self.base.cache[env] = {
            "data": data,
            "form": env
        }
