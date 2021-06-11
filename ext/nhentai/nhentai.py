from structure.extensions import NatsumeExt
from structure.nhentaiAPI import Hentai, TagOption, Page, Tag, Sort
from structure.utils import NatsumeUtils

class NatsumeDivineObj(NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "hentai"
        self.desc = "Come, Join US to the AHHH side"
        self.help = "TBA"

        self.hentai = Hentai()
        self.utils = NatsumeUtils()

    def execute(self, args):
        return super().execute(args)