import sqlite3
import time
import requests
import re
import random

wear_map = { "Battle-Scarred": 1, "Well-Worn": 2, "Field-Tested": 3, "Minimal Wear": 4, "Factory New": 5 }
quality_map = { "7D6D00": 1, "476291": 2, "4D7455": 3, "CF6A32": 4, "8650AC": 5, "38F3AB": 6, "AA0000": 7, "FAFAFA": 8, "70B04A":9 }

def run():
    # Initializing the database for this script.
    with sqlite3.connect("data/steam_community_market.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS tf2_items(
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
                     """)
            
    conn.cursor().execute(
        "INSERT OR IGNORE INTO metadata (table_name, refresh_window) VALUES (?, ?)", ("tf2_items", 1209600))
    conn.commit()

    # Here we start by initializing the state. Last page visited is stored in the db. This way we can always resume where left off.
    with sqlite3.connect("data/steam_community_market.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_index_visited, refresh_window, last_updated FROM metadata WHERE table_name == 'tf2_items'")
        row = cursor.fetchone()
        page = row[0] # Here we get the index of where to resuem
        period = row[1] # Here we get the update window to check if updates are needed.
        lastUpdated = row[2] # Here we get the time of the last time the table was updated.

    # Checking if data is outdated, will finish early if no update is needed yet.
    current_time = int(time.time())
    if (current_time - lastUpdated) < period:
        print("No update needed yet. Exiting early.")
        return
        
    start_time = int(time.time()) # start timer
    while True:
        url = f"https://steamcommunity.com/market/search/render/?query=&norender=1&start={page}&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=440"
        
        try:
            response = requests.get(url,timeout=10)
            response.raise_for_status()
            data = response.json()

            total_count = data.get("total_count") # requiers a sucessful connect to initilize the total_count, otherwise cant print
            results = data.get("results")

            with sqlite3.connect("data/steam_community_market.db") as conn:
                cursor = conn.cursor()

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
                    wear = _getWear(name)
                    quality = _getQuality(i.get("asset_description",{}).get("name_color")) 
                    strange = _isStrange(name)
                    killstreak = _getKillstreak(name)
                    festivized = _isFestivized(name)
                    limited = _isLimited(description)
                    taunt = _isTaunt(name)
                    last_updated = int(time.time())

                    cursor.execute("""
                        INSERT INTO tf2_items(
                                   name,
                                   sell_listings,
                                   sell_price,
                                   classid,
                                   instanceid,
                                   type,
                                   commodity,
                                   wear,
                                   quality,
                                   strange,
                                   killstreak,
                                   festivized,
                                   limited,
                                   taunt,
                                   last_updated
                                   )
                                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                   ON CONFLICT(name) DO UPDATE SET
                                   sell_listings = excluded.sell_listings,
                                   sell_price = excluded.sell_price,
                                   classid = excluded.classid,
                                   instanceid = excluded.instanceid,
                                   type = excluded.type,
                                   commodity = excluded.commodity,
                                   wear = excluded.wear,
                                   quality = excluded.quality,
                                   strange = excluded.strange,
                                   killstreak = excluded.killstreak,
                                   festivized = excluded.festivized,
                                   limited = excluded.limited,
                                   taunt = excluded.taunt,
                                   last_updated  = excluded.last_updated
                                   """,(name, sell_listings, sell_price, classid, instanceid, description,
                                        commodity, wear, quality, strange, killstreak, festivized, limited,
                                        taunt, last_updated))

                page += 10
                cursor.execute( "UPDATE metadata SET last_index_visited = ? WHERE table_name = ?", (page, "tf2_items",) )
            
            #wait and random jitter
            _wait(request_count=page/10)

            if page > total_count: # Here if the current page we are one is larger than the total pages, all have been visited.
                break
        
        except requests.exceptions.HTTPError as e: # Handles HTTP errors and deals with rate limiting
            print("HTTP error:", e)
            if e.response.status_code == 429: 
                print("Rate limit hit, backing off...")
                _wait(3,page/10) # much longer wait
            elif e.response.status_code == 403:
                print("Forbidden. Not retrying.")
                return
            elif e.response.status_code >= 500:
                print("Server error, retrying...")
                _wait(2,page/10) # moderate wait
            else: print("Other HTTP error:", e)
        except requests.exceptions.ConnectionError as e: # Handles couldnt reach the server
            print("Connection error:", e)
        except requests.exceptions.Timeout as e: # Handles not getting a response from he server
            print("Timeout error:", e)
        except requests.exceptions.RequestException as e: # Handles anything else
            print("Unexpected error:", e)

        # Prints progress and passed time to console each loop, not in the best way but workable for now
        time_passed = int(time.time()) - start_time
        print(f"Progress: {page/10}/{total_count/10}\t{page/total_count}%\tTime elapsed: {time_passed}")
    
    #we made it out of the loop and to the end of the function, update stat to reflect success and initilize for future updates
    with sqlite3.connect("data/steam_community_market.db") as conn:
        cursor = conn.cursor()
        cursor.execute( "UPDATE metadata SET last_index_visited = ?, last_updated = ? WHERE table_name = ?", (0, int(time.time()), "tf2_items") )

    

if __name__ == "__main__":
    run() # only runs when executed directly

def _getWear(name):  # will be determined from name
    # wear will 0-5, 0 = no wear, 1=bs - 5=fn
    match = re.search(r"\((.*?)\)", name)
    if match:
        wear_str = match.group(1)
        return wear_map.get(wear_str,0)
    
    return 0

def _getQuality(hex): # will be determined by text color hex value provided
    # unique = "7D6D00", vintage = "476291", genuine = "4D7455", strange = "CF6A32", unusual = "8650AC", haunted = "38f3ab", collectors = "AA0000"
    # decorated = "FAFAFA", self made = "70B04A"
    return quality_map.get(hex.upper(), 0)

def _isStrange(name: str) -> bool: # will be determined by name, if name begins with strange
    # if name contains strange, will be marked as strange, not perfect it will do
    return True if re.search(r"\bStrange\b", name) else False

def _getKillstreak(name): # will be determined by name if it meets right criteria
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

def _isFestivized(name): # well be determined by name
    # if name contains festivized, will be marked as such
    return True if re.search(r"\bFestivized\b", name) else False

def _isLimited(description): # will be determined by descriptoin if contains the word limited
    return True if re.search(r"\bLimited\b", description) else False

def _isTaunt(name): # will be determined by name
    # matches with 'taunt:' in name
    return True if re.search(r"\bTaunt: \b", name) else False

def _wait(offset: int = 0, request_count: int = 0): # function responsible for determining delay between calls
    # Base range for normal success case
    #it was found that, at low values 25 pages were coverd in 60s followed by 3min45s before resuming. this patter carried for a bit before 429 became too common.
    #it seems an avg of 13s per page request keeps 429s really low.
    #piror tested valued were 9.6 - 12.8, the avg wait should be around 12.8 ~13s
    base_min = 11.6 #with 11.6 - 13.8 & jitter = 0.2 was able to get 574 pages done in 7750s before 429 with ~13.5s/page, seems to have hit a larger limmit, 6-7 hour ban
    base_max = 13.8

    # Scale up by offset, offsett acts as a multiplier to the min and max delay times.
    delay = random.uniform(base_min, base_max) * (1 + offset)
    # Add jitter (+/- 200ms)
    jitter = random.uniform(-0.25, 0.25) #was 0.2 before
    
    final_delay = max(0, delay + jitter)

    # Periodic longer delay every 20–40 requests
    """if request_count % random.randint(20, 40) == 0 and request_count > 0: 
        extra_delay = random.uniform(5, 10) 
        final_delay += extra_delay"""
    
    time.sleep(final_delay)

