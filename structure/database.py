from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.schema import Table
from . import utils

BaseModel = declarative_base()

class NatsumeDatabase:
    def __init__(self):
        self.name = "NatsumeMainDatabase"
        self.utils = utils.NatsumeUtils()
        self.config = self.utils.getConfig()["database"]
        self.engine = create_engine(self.config["url"])
        self.session = sessionmaker(bind=self.engine)
        self.tables = []
    
    def configure_table(self, tables: List[Table]):
        self.tables.extend(tables)
    
    def create_db(self):
        BaseModel.metadata.drop_all(self.engine)
        BaseModel.metadata.create_all(self.engine)