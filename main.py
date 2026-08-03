import os
import sqlite3

from scripts import update_local_market

def main():
    print("Welcome to the market creator")

    with sqlite3.connect("data/steam_community_market.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS metadata(
            table_name TEXT PRIMARY KEY,
            schema_version INTEGER DEFAULT 1,
            last_index_visited INTEGER DEFAULT 0,
            refresh_window INTEGER DEFAULT 604800,
            last_updated INTEGER DEFAULT 0
            );
        """)

    status = update_local_market.run()

if __name__ == "__main__":
    main()