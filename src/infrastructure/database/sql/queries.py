INSERT_METADATA = """--sql
INSERT INTO metadata (table_name, refresh_window)
VALUES (?, ?)
ON CONFLICT(table_name) DO NOTHING;
"""
