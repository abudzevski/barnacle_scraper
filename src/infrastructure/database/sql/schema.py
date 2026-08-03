CREATE_METADATA_TABLE = """--sql
CREATE TABLE IF NOT EXISTS metadata (
    table_name TEXT PRIMARY KEY,
    schema_version INTEGER DEFAULT 1,
    resume_index INTEGER DEFAULT 0,
    refresh_window INTEGER DEFAULT 604800,
    last_updated INTEGER DEFAULT 0
);
"""

CREATE_TF2_ITEMS_TABLE = """--sql
CREATE TABLE IF NOT EXISTS tf2_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    sell_listings INTEGER DEFAULT NULL,
    sell_price INTEGER DEFAULT NULL,
    classid TEXT DEFAULT NULL,
    instanceid TEXT DEFAULT NULL,
    type TEXT DEFAULT NULL,
    commodity BOOLEAN DEFAULT false,
    item_nameid TEXT DEFAULT NULL,
    wear INTEGER DEFAULT NULL,
    quality INTEGER DEFAULT NULL,
    strange BOOLEAN DEFAULT false,
    killstreak INTEGER DEFAULT NULL,
    festivized BOOLEAN DEFAULT false,
    limited BOOLEAN DEFAULT false,
    taunt BOOLEAN DEFAULT false,
    last_updated INTEGER DEFAULT NULL
);
"""

CREATE_TF2_PRICE_TRENDS_TABLE = """--sql
CREATE TABLE IF NOT EXISTS tf2_price_trends (
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
"""

SCHEMA = [CREATE_METADATA_TABLE, CREATE_TF2_ITEMS_TABLE, CREATE_TF2_PRICE_TRENDS_TABLE]

__all__ = ["SCHEMA"]