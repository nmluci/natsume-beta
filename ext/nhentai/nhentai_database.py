from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from structure.database import BaseModel

class HentaiTitle(BaseModel):
    __tablename__ = "HentaiTitle"

    id = Column(Integer, primary_key=True)
    eng = Column(Text, nullable=False)
    jp = Column(Text, nullable=False)
    pretty = Column(Text, nullable=False)

class HentaiSeries(BaseModel):
    __tablename__ = "HentaiSeries"

    id = Column(Integer, primary_key=True)
    series_name = Column(Text, nullable=False)

class HentaiBook(BaseModel):
    __tablename__ = "HentaiBook"

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey(HentaiSeries.id, ondelete="SET NULL", onupdate="CASCADE"))
    title_id = Column(Integer, ForeignKey(HentaiTitle.id, ondelete="SET NULL", onupdate="CASCADE"))
    thumbnail = Column(Text, nullable=False)
    cover = Column(Text, nullable=False)
    scanlator = Column(Text, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    epoch_time = Column(Integer, nullable=False)
    language = Column(Text, nullable=False)
    num_page = Column(Integer, nullable=False, default=0)

class HentaiTagType(BaseModel):
    __tablename__ = "HentaiTagType"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

class HentaiTag(BaseModel):
    __tablename__ = "HentaiTag"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey(HentaiBook.id, ondelete="SET NULL", onupdate="CASCADE"))
    type_id = Column(Integer, ForeignKey(HentaiTagType.id, ondelete="SET NULL", onupdate="CASCADE"))
