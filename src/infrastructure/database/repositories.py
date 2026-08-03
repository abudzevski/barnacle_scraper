from database import Database
#from sql_queries import *
#import sql_queries as q

class MetadataRepository:
    def __init__(self, db: Database):
        self.db = db
		
class ListingRepository:
    def __init__(self, db: Database):
        self.db = db
		
class ItemRepository:
    def __init__(self, db: Database):
        self.db = db