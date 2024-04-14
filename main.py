from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scraper import NbaTriviaSpider
from database import MongoDBHandler 

class ItemCollectorPipeline:
    def __init__(self, store_in_db):
        self.store_in_db = store_in_db

    @classmethod
    def from_crawler(cls, crawler):
        # This method is a class method to instantiate the pipeline from settings
        return cls(store_in_db=crawler.settings.getbool('STORE_IN_DB'))

    def open_spider(self, spider):
        if self.store_in_db:
            self.db_handler = MongoDBHandler(mongo_db='test', mongo_collection='players')

    def process_item(self, item, spider):
        if self.store_in_db:
            self.db_handler.insert_record('players', dict(item))
        else:
            print(item)
        return item

    def close_spider(self, spider):
        if self.store_in_db:
            self.db_handler.close()

def run_spider(store_in_db=False):
    # Setup Scrapy settings including the item pipeline
    settings = {
        'ITEM_PIPELINES': {'__main__.ItemCollectorPipeline': 100},
        # You can add custom settings if required, such as:
        'STORE_IN_DB': store_in_db,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(NbaTriviaSpider)
    process.start() 

# Set 'store_in_db' to True to store items in the database, or False to print them
run_spider(store_in_db=True)