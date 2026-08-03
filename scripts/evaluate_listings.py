import sqlite3

def run():
    # Initializing the database for this script.
    with sqlite3.connect("data/steam_community_market.db") as conn: #new table schema goes here
        conn.execute("""CREATE TABLE IF NOT EXISTS tf2_price_trends(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     tf2_items_id INTEGER NOT NULL,
                     mean_price REAL DEFAULT NULL,
                     sd REAL DEFAULT NULL,
                     sd_up REAL DEFAULT NULL,
                     sd_down REAL DEFAULT NULL,
                     transactions INTEGER DEFAULT NULL,
                     min_buying_price REAL DEFAULT NULL,
                     max_selling_price REAL DEFAULT NULL,
                     local_max REAL DEFAULT NULL,
                     local_min REAL DEFAULT NULL,
                     current_price REAL DEFAULT NULL,
                     score REAL DEFAULT NULL,
                     profit REAL DEFAULT NULL,
                     profit_margin REAL DEFAULT NULL,
                     last_updated INTEGER DEFAULT NULL,
                     FOREIGN KEY (tf2_items_id) REFERENCES tf2_items(id) ON DELETE CASCADE
                     );
                     """)
            
    conn.cursor().execute(
        "INSERT OR IGNORE INTO metadata (table_name, refresh_window) VALUES (?, ?)", ("tf2_price_trends", 1209600))
    conn.commit()

if __name__ == "__main__":
    run() # only runs when executed directly