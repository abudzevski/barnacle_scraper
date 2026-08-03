import os
import sqlite3
from sql_schema import SCHEMA
from sql_queries import INSERT_METADATA

class Connection:
    def __init__(self):
        self.folder = "data"
        self.db_name = "tf2_market.db"
        self.db_path = os.path.join(self.folder, self.db_name)

        # Makes sure db path exists.
        os.makedirs(self.folder, exist_ok=True)

        # Makes sure tables exists and are ready to use.
        self._ensure_initialized()

    def _ensure_initialized(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        for statement in SCHEMA:
            cursor.execute(statement)
        # Initializes the metadata table with defaul values per table.
        # This should only happen if no prior records existed, ideally, when the program first runs.
        cursor.execute(INSERT_METADATA, ("tf2_items", 1209600))
        cursor.execute(INSERT_METADATA, ("tf2_price_trends", 1209600))
        conn.commit()
        conn.close()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn