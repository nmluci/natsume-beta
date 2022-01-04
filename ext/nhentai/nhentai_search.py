from structure import extensions
from structure.nhentaiAPI import Book, Hentai
from structure.download import ExtDownloader

class NatsumeDivineObjSearch(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "nhentai-search"
        self.desc = "Come, Find Us"
        self.alias = ["hentai-search", "nh-search"]
        self.args = [
            {
                "name": "query",
                "type": str,
                "desc": "search book"
            }
        ]
        self.isSystem = False
        self.hentai = Hentai()
        
    def execute(self, **args):
        return super().execute(args=args)
