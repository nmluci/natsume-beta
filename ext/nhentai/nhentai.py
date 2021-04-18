from structure import extensions
import urllib

class NatsumeNHentaiAPI(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "nhentaiman"
        self.isSystem = True
        self.desc = "Master's own implementation of nHentai API based on publicly known API endpoints"
        self.help = "..."
        self.baseURL = "https://www.nhentai.net/g/"

    def execute(self, args):
        return super().execute(args)

    def getSauce(self, id):
        return self.execute()