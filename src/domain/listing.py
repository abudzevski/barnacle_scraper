from dataclasses import dataclass

@dataclass(frozen=True)
class Listing:
    name: str | None = None
    sell_listings: int | None = None
    sell_price: int | None = None
    classid: str | None = None
    instanceid: str | None = None
    type: str | None = None
    commodity: bool | None = None
    item_nameid: str | None = None
    wear: int | None = None
    quality: int | None = None
    strange: bool | None = None
    killstreak: int | None = None
    festivized: bool | None = None
    limited: bool | None = None
    taunt: bool | None = None
    last_updated: int | None = None