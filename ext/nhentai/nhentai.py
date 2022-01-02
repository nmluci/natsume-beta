from __future__ import annotations
from typing import List
from datetime import datetime

from ext.nhentai.nhentai_database import HentaiBook, HentaiTag, HentaiTitle, HentaiTagType

from structure import extensions
from structure.nhentaiAPI import Book, Hentai
from structure.download import ExtDownloader

class NatsumeDivineObj(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "nhentai"
        self.desc = "Come, Join US to the AHHH side"
        self.help = "Come, Join US to the AHHH side"
        self.alias = ["hentai", "nh", "doujin"]
        self.args = [
            {
                "name": "id",
                "type": str,
                "desc": "BookID"
            }, 
            {
                "name": "isDownload",
                "type": str,
                "desc": "download?",
                "default": "no",
                "optional": True
            }
        ]
        self.isSystem = False
        self.hentai = Hentai()
        self.dler = ExtDownloader()
        
    def execute(self, id, isDownload):
        try:
            book = self.hentai.getDoujin(id)
            self.importDoujin(book)
            self.printDoujinInfo(book, True if isDownload.lower() == "yes" else False)
        except Exception as e:
            self.utils.printError("nh", f"An Error Occured: {e}")

    def importDoujin(self, doujin: Book):
        try:
            session = self.session()
            rawTag =  doujin.rawTag

            title = HentaiTitle(eng=doujin.title.eng, jp=doujin.title.jp, pretty=doujin.title.pretty)
            session.add(title)
            for tag in filter(lambda t: (t.type=="tag"), rawTag):
                if not session.query(HentaiTagType).filter(HentaiTagType.id==tag.id).first():
                    newTag = HentaiTagType(id=tag.id, name=tag.name)
                    session.add(newTag)
                    
                if not session.query(HentaiTag).filter((HentaiTag.id==tag.id) & (HentaiTag.book_id==doujin.id)):
                    newBookTag = HentaiTag(book_id=doujin.id, type_id=tag.id)
                    session.add(newBookTag)
            
            approxTitleId = session.query(HentaiTitle).order_by(HentaiTitle.id.desc()).first()

            if not session.query(HentaiBook).filter(HentaiBook.id==doujin.id):
                newBook = HentaiBook(id=doujin.id, 
                                    title_id=approxTitleId.id, 
                                    thumbnail=doujin.thumbnail, 
                                    cover=doujin.cover, 
                                    scanlator=doujin.scanlator,
                                    upload_date=datetime.fromtimestamp(doujin.epoch),
                                    epoch_time=doujin.epoch,
                                    language=doujin.lang,
                                    num_page=doujin.num_pages)
                session.add(newBook)
        except Exception as e:
            self.utils.printError("nh-importer", f"An Database Error Occured: {e}")
            self.utils.printInfo('nh-importer', "rolling back changes")
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
            
    def downloadDoujin(self, doujin: Book):
        urlList = list()
        for page in doujin.pages:
            urlList.append(page.url)
        self.dler.downloader(urlList, f"nhentai-{doujin.id}")

    def printDoujinInfoCompact(self, doujin: List[Book]):
        for num, book in enumerate(doujin):
            print("{}({}) [{}] {}{}"
                .format(self.utils.BLUE, num, book.id, book.title.pretty, self.utils.CLR))

    def printDoujinInfo(self, doujin: Book, dlconfirm: str):
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "ID", doujin.id, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Title", doujin.title.pretty, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Character", doujin.character, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Pages", doujin.num_pages, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Tags", doujin.tags, self.utils.CLR))
        print("{}{:<10}: {}{}".format(self.utils.BLUE, "Lang", doujin.lang, self.utils.CLR))

        if dlconfirm:
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
