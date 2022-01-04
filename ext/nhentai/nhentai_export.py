from datetime import datetime
from pathlib import Path

from ext.nhentai.nhentai_database import HentaiBook, HentaiSeries, HentaiTag, HentaiTagType, HentaiTitle
from structure import extensions

class NatsumeDivineObjExporter(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "nhentai-export"
        self.desc = "Come, Expose Us"
        self.alias = ["hentai-export", "nh-export"]
        self.args = [
            {
                "name": "exportloc",
                "type": str,
                "desc": "exported location",
                "optional": True,
                "default": "hentai-export.json"
            }
        ]
        self.isSystem = False
        self.saveLocation:Path = None

    def exportFromDatabase(self):
        pass

    def execute(self, exportloc):
        self.saveLocation = Path(exportloc)
        session = self.session()
        
        if not session.query(HentaiBook).count():
            self.utils.printError("hentai-export", "database has no hentai data")
        else:
            super().execute()
    