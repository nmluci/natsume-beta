from datetime import datetime
from typing import List
import re
from ext.nhentai.nhentai_database import HentaiBook, HentaiTag, HentaiTagType, HentaiTitle

from structure import extensions
from structure.nhentaiAPI import Book, Hentai
from ext.filehandling.ext.tachiyomi.compiled.TachiyomiBackup import BackupManga

class NatsumeDivineObjImporter(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "nhentai-import"
        self.desc = "Come, Find Us"
        self.alias = ["hentai-import", "nh-import"]
        self.isSystem = False
        self.hentai = Hentai()
        self.added = 0

    # fallback in case manga not available anymore
    def importFromTachiyomiFallback(self, manga: BackupManga, ctr):
        try:
            session = self.session()
            bookId = re.findall(r"\d+", manga.url)[0]

            for tag in manga.genre:
                tagData = session.query(HentaiTagType).filter(HentaiTagType.name==tag).first()
                if not tagData:
                    self.utils.printError("hentai-import (fallback)", f"{tag} has no related data")
                else:
                    if not session.query(HentaiTag).filter((HentaiTag.type_id==tagData.id) & (HentaiTag.book_id==bookId)).first():
                        newBookTag = HentaiTag(book_id=bookId, type_id=tagData.id)
                        session.add(newBookTag)

            newTitle = HentaiTitle(eng=manga.title, jp=manga.title, pretty=manga.title)
            session.add(newTitle)

            approxTitleId = session.query(HentaiTitle).order_by(HentaiTitle.id.desc()).first()
            newBook = HentaiBook(id=bookId, 
                                title_id=approxTitleId.id,
                                thumbnail=manga.thumbnail_url,
                                cover=manga.thumbnail_url,
                                scanlator=manga.chapters[0].scanlator,
                                upload_date=datetime.fromtimestamp(manga.chapters[0].date_upload/1000),
                                epoch_time=manga.chapters[0].date_upload/1000,
                                language="english",
                                num_page=manga.chapters[0].chapter_number)
            session.add(newBook)
            self.utils.printInfo("hentai-import (fallback)", f"{ctr} found new title: <{bookId}> {manga.title}")
        except Exception as e:
            self.utils.printError("hentai-import (fallback)", e)
            session.rollback()
        else:
            session.commit()
            session.close()
            self.added += 1

    
    def importFromTachiyomi(self, bookshelf: List["BackupManga"]):
        try:
            self.added = 0
            for ctr, book in enumerate(bookshelf):
                session = self.session()
                bookId = re.findall(r"\d+", book.url)[0]

                try:
                    book = self.hentai.getDoujin(bookId)
                    if session.query(HentaiBook).filter(HentaiBook.id==book.id).first():
                        self.utils.printInfo("hentai-import", f"id {book.id} already indexed")
                        continue

                except ValueError as e:
                    self.utils.printError("hentai-import", f"a hentai gathering error occured, using fallback strategies")
                    self.importFromTachiyomiFallback(book, ctr)
                    continue

                for tag in filter(lambda t: (t.type=="tag"), book.rawTag):
                    if not session.query(HentaiTagType).filter(HentaiTagType.id==tag.id).first():
                        newTag = HentaiTagType(id=tag.id, name=tag.name)
                        session.add(newTag)

                        self.utils.printInfo("hentai-import", f"added new tag: <{tag.id}> {tag.name}")
                    if not session.query(HentaiTag).filter((HentaiTag.type_id==tag.id) & (HentaiTag.book_id==book.id)).first():
                        newBookTag = HentaiTag(book_id=book.id, type_id=tag.id)
                        session.add(newBookTag)
                
                title = HentaiTitle(eng=book.title.eng, jp=book.title.jp, pretty=book.title.pretty)
                session.add(title)

                approxTitleId = session.query(HentaiTitle).order_by(HentaiTitle.id.desc()).first()
                newBook = HentaiBook(id=book.id, 
                                    title_id=approxTitleId.id,
                                    thumbnail=book.thumbnail,
                                    cover=book.cover,
                                    scanlator=book.scanlator,
                                    upload_date=datetime.fromtimestamp(book.epoch),
                                    epoch_time=book.epoch,
                                    language=book.lang,
                                    num_page=book.num_pages)
                session.add(newBook)
                self.utils.printInfo("hentai-import", f"{ctr} found new title: <{book.id}> {book.title.pretty}")

                session.commit()
                session.close()
                self.added += 1

        except Exception as e:
            self.utils.printError("hentai-import", f"an database error occured: {e}")
            self.utils.printError("hentai-import", "rolling back database")
            session.rollback()
        
    def execute(self):
        try:
            if (len(self.base.cache) == 0) or 'mangaBackup' not in self.base.cache.keys():
                return self.utils.printInfo("hentai-import", "please load the file first as 'manga_backup'")
            
            self.importFromTachiyomi(self.base.cache["mangaBackup"]["data"]["doujin"])        
        except Exception as e:
            self.utils.printError("hentai-import", f"an error occured: {e}")
        else:
            self.utils.printInfo("hentai-import", f"Newly added hentai: {self.added}")
