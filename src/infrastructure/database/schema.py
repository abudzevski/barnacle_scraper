from dataclasses import dataclass

@dataclass(frozen=True)
class _MetadataTable:
    NAME: str = "metadata"
    PK_TABLE: str = "table_name"
    COL_SCHEMA_VERSION: str = "schema_version"
    COL_INDEX: str = "cursor"
    COL_PERIOD: str = "refresh_interval"
    COL_LAST_UPDATED: str = "updated_at"

@dataclass(frozen=True)
class _ItemsTable:
    NAME: str = "listings"
    PK_ID: str = "id"
    COL_ITEM: str = "item_name"
    COL_LISTINGS: str = "sell_listings"
    COL_PRICE: str = "sell_price"
    COL_CLASSID: str = "classid"
    COL_INSTANCEID: str = "instanceid"
    COL_DESC: str = "type"
    COL_COMMODITY: str = "commodity"
    COL_ITEM_ID: str = "item_nameid"
    COL_WEAR: str = "wear"
    COL_QUALITY: str = "quality"
    COL_STRANGE: str = "strange"
    COL_KILLSTREAK: str = "killstreak"
    COL_FESTIVIZED: str = "festivized"
    COL_LIMITED: str = "limited"
    COL_TAUNT: str = "taunt"
    COL_LAST_UPDATED: str = "updated_at"

@dataclass(frozen=True)
class _PriceTable:
    NAME: str = "items"
    PK_ID: str = "id"
    FK_ITEM_ID: str = "listing_id"
    COL_MEAN: str = "mean_price"
    COL_SD: str = "sd"
    COL_SD_UP: str = "sd_up"
    COL_SD_DOWN: str = "sd_down"
    COL_TRANSACTIONS: str = "transactions"
    COL_BUY_AT: str = "min_buying_price" #buying_floor
    COL_SELL_AT: str = "max_selling_price" #selling_ceiling
    COL_LOCAL_MAX: str = "local_max"
    COL_LOCAL_MIN: str = "local_min"
    COL_LAST_SOLD_AT: str = "current_price"
    COL_SCORE: str = "score"
    COL_PROFIT: str = "profit"
    COL_PROFIT_MARGIN: str = "profit_margin"
    COL_LAST_UPDATED: str = "updated_at"

@dataclass(frozen= True)
class DatabaseSchema:
    DB_NAME: str = "tf2_market.db"
    META: _MetadataTable = _MetadataTable()
    ITEMS: _ItemsTable = _ItemsTable()
    PRICE: _PriceTable = _PriceTable()

__all__ = ["DatabaseSchema"]