from schema import DatabaseSchema
from database import Database
from metadata_repository import MetadataRepository
from tf2_items_repository import ItemsRepository
from tf2_price_trends_repository import TrendsRepository
from network.tf2_market_client import Tf2MarketClient
from network.tf2_item_client import Tf2ItemClient
from network.tf2_itemid_client import Tf2ItemidClient
from update_market import MaintainMarket

def main():
    
    db = Database()
    meta_repo = MetadataRepository(db)
    items_repo = ItemsRepository(db)
    trends_repo = TrendsRepository(db)

    market_net = Tf2MarketClient()
    listing_net = Tf2ItemClient()
    itemid_net = Tf2ItemidClient()
    
    market = MaintainMarket(meta_repo=meta_repo, items_repo=items_repo, network=market_net)
    select = None
    analyze = None

    market()
	
def altMain(): # what main should probably look like
	db = DatabaseConnection()
	
	listing_repo = ListingRepository(db)
	item_repo = ItemRepository(db)
	metadata_repo = MetadataRepository(db)
	
	listing_client = ListingClient()
	item_client = ItemClient()
	orders_client = OrdersClient()
	
	update_listings = UpdateListings(listing_client, listing_repo, metadata_repo)
	select_items = SelectItems(listing_repo, item_repo)
	analyze_items = AnalyzeItems(item_client, orders_client, item_repo, metadata_repo)
	
	update_listings.execute()
	select_items.execute()
	analyze_items.execute()


if __name__ == "__main__":
    main()