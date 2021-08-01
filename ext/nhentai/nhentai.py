from __future__ import annotations
from typing import List

from structure import extensions
from structure.nhentaiAPI import Book, Hentai, TagOption, Page, Tag, Sort
from structure.download import ExtDownloader
import sys

class NatsumeDivineObj(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "nhentai"
        self.desc = "Come, Join US to the AHHH side"
        self.help = "Come, Join US to the AHHH side"
        self.alias = ["hentai", "nh", "doujin"]
        self.args = [
            {
                "name": "id",
                "type": str,
                "desc": "BookID"
            }
        ]
        self.isSystem = False
        self.hentai = Hentai()
        self.dler = ExtDownloader()
        
    def execute(self, args: List[str]):
        try:
            if len(args) == 1:
                if self.utils.isDigit(args[0]):
                    book = self.hentai.getDoujin(int(args[0]))
                    self.printDoujinInfo(book)
                elif args[0] == "random" or args[0] == "rand":
                    book = self.hentai.random()
                    self.printDoujinInfo(book)
                elif args[0] == "help":
                    self.helpMenu()
                else:
                    return super().execute(args)
            elif args[0].lower() == "search": self.searchDoujin(args)
            else:
                super().execute()
        except Exception as e:
            self.utils.printError("nh", f"An Error Occured: {e}")

    def downloadDoujin(self, doujin: Book):
        urlList = list()
        for page in doujin.pages:
            urlList.append(page.url)
        self.dler.downloader(urlList, f"nhentai-{doujin.id}")

    def printDoujinInfoCompact(self, doujin: List[Book]):
        for num, book in enumerate(doujin):
            print("{}({}) [{}] {}{}"
                .format(self.utils.BLUE, num, book.id, book.title.pretty, self.utils.CLR))

    def printDoujinInfo(self, doujin: Book):
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "ID", doujin.id, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Title", doujin.title.pretty, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Character", doujin.character, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Pages", doujin.num_pages, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Tags", doujin.tags, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Lang", doujin.lang, self.utils.CLR))

        dlconfirm = input("Download? ")
        if "yes" == dlconfirm:
            try:
                nukecode = doujin.id
            except IndexError:
                self.utils.printError("nh", "invalid number entered!")
            except Exception as e:
                self.utils.printError("nh", f"Another Exception Occured: {e}")
            else:
                self.downloadDoujin(self.hentai.getDoujin(nukecode))

    def searchDoujin(self, args, all=False):
        try: 
            page = args[args.index("page") + 1]
            query = "+".join(args[1:args.index("page")]).replace("\"", "")
        except ValueError:
            page = 1
            query = "+".join(args[1:]).replace("\"", "")
        
        print("{}Page: {} {}".format(self.utils.BLUE, page, self.utils.CLR))
        if not all:
            res = self.hentai.search(query, page)
        else:
            return super().execute()

        self.printDoujinInfoCompact(res)

        infoConfirm = input("Open: ");
        if self.utils.isDigit(infoConfirm):
            try:
                self.printDoujinInfo(res[int(infoConfirm)])
            except IndexError:
                self.utils.printError("nh", "Invalid index number entered!")
