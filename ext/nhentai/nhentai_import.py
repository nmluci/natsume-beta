from structure import extensions
from structure.nhentaiAPI import Book, Hentai
from structure.download import ExtDownloader

class NatsumeDivineObjImporter(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "nhentai-import"
        self.desc = "Come, Find Us"
        self.alias = ["hentai-import", "nh-import"]
        self.isSystem = False
        self.hentai = Hentai()
        
    def execute(self, args=None):
        if len(self.base.cache) == 0:
            return super().execute(args=args)
        else:
            return self.utils.printInfo("fuee")
