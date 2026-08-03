from network.base_client import BaseNetworkClient
from network.dto import NetworkDTO
from tf2_item_model import ItemRecord
from dataclasses import field
import json
import re
import time

class ListingClient(BaseClient):
    
    _wear_map = {
        "Battle-Scarred": 1,    # worst condition
        "Well-Worn": 2,         # pretty rough
        "Field-Tested": 3,      # mid-tier
        "Minimal Wear": 4,      # almost clean
        "Factory New": 5        # best condition
    }
    _quality_map = {
        "7D6D00": 1,    # unique    
        "476291": 2,    # vintage
        "4D7455": 3,    # genuine
        "CF6A32": 4,    # strange
        "8650AC": 5,    # unusual
        "38F3AB": 6,    # haunted
        "AA0000": 7,    # collectors
        "FAFAFA": 8,    # decorated
        "70B04A":9      # self made
    }

    def _fetch_raw(self, dst):
        return f"https://steamcommunity.com/market/search/render/?query=&norender=1&start={dst}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=440"

    def _parse(self, raw_text):
        raw = json.loads(raw_text)

        # requiers a sucessful connect to initilize the total_count, otherwise cant print
        total_count = raw.get("total_count")
        data: list = field(default_factory=list)
        
        results = raw.get("results")
        

        for i in results:
            name = i.get("name")
            if name is None:
                continue # skip incomplete rows
            sell_listings = i.get("sell_listings")
            sell_price = i.get("sell_price")
            classid = i.get("asset_description",{}).get("classid")
            instanceid = i.get("asset_description",{}).get("instanceid")
            description = i.get("asset_description",{}).get("type")
            commodity = i.get("asset_description",{}).get("commodity")
            wear = self._getWear(name)
            quality = self._getQuality(i.get("asset_description",{}).get("name_color")) 
            strange = self._isStrange(name)
            killstreak = self._getKillstreak(name)
            festivized = self._isFestivized(name)
            limited = self._isLimited(description)
            taunt = self._isTaunt(name)
            last_updated = int(time.time())

            item = ItemRecord(
                name=name,
                sell_listings=sell_listings,
                sell_price=sell_price,
                classid=classid,
                instanceid=instanceid,
                type=description,
                commodity=commodity,
                wear=wear,
                quality=quality,
                strange=strange,
                killstreak=killstreak,
                festivized=festivized,
                limited=limited,
                taunt=taunt,
                last_updated=last_updated
            )

            data.append(item)

        return NetworkDTO(
            success=True,
            data=data,
            total_count=total_count
        )



    def _getWear(self, name):  # will be determined from name
        # wear will 0-5, 0 = no wear, 1=bs - 5=fn
        match = re.search(r"\((.*?)\)", name)
        if match:
            wear_str = match.group(1)
            return self._wear_map.get(wear_str,0)
        
        return 0
    
    def _getQuality(self, hex): # will be determined by text color hex value provided
    
        return self.quality_map.get(hex.upper(), 0)

    def _isStrange(self, name: str) -> bool: # will be determined by name, if name begins with strange
        # if name contains strange, will be marked as strange, not perfect it will do
        return True if re.search(r"\bStrange\b", name) else False

    def _getKillstreak(self, name): # will be determined by name if it meets right criteria
        # killstreak will 0 - 8, 0 = no killstreak, 1=ks,2=sks, 3=pks, 4=ks kit, 5=sks kit, 6 =pks kit, 7 = sks kit fab, 8 = pks fab
        if re.search(r"Professional Killstreak .* Kit Fabricator", name):
            return 8
        elif re.search(r"Specialized Killstreak .* Kit Fabricator", name):
            return 7
        elif re.search(r"Professional Killstreak .* Kit", name):
            return 6
        elif re.search(r"Specialized Killstreak .* Kit", name):
            return 5
        elif re.search(r"Killstreak .* Kit", name):
            return 4
        elif re.search(r"Professional Killstreak", name):
            return 3
        elif re.search(r"Specialized Killstreak", name):
            return 2
        elif re.search(r"Killstreak", name):
            return 1
        else:
            return 0

    def _isFestivized(self, name): # well be determined by name
        # if name contains festivized, will be marked as such
        return True if re.search(r"\bFestivized\b", name) else False

    def _isLimited(self, description): # will be determined by descriptoin if contains the word limited
        return True if re.search(r"\bLimited\b", description) else False

    def _isTaunt(self, name): # will be determined by name
        # matches with 'taunt:' in name
        return True if re.search(r"\bTaunt: \b", name) else False
