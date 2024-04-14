import os
import scrapy
from items import Nba2kRatingItem, PlayerItem
from pymongo import MongoClient

class NbaTriviaSpider(scrapy.Spider):
    name = 'nba_trivia'
    first_year = 2011
    last_year = 2023

    def __init__(self):
        # MongoDB setup
        self.mongo_uri = os.getenv('MONGO_URI')
        self.mongo_db = os.getenv('MONGO_DATABASE', 'test')
        self.mongo_collection = os.getenv('MONGO_COLLECTION', 'players')
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def start_requests(self):
        base_url = 'https://hoopshype.com/nba2k/{}-{}'
        for year in range(self.first_year, self.last_year + 1):
            url = base_url.format(year, year + 1)
            yield scrapy.Request(url=url, callback=self.parse, meta={'year': year})

    def parse(self, response):
        # table = response.xpath('//div[contains(@class, "hh-salaries-ranking-table")]//table')
        # table = response.css('div.hh-salaries-ranking-table table')
        table = response.css('table.hh-salaries-ranking-table.hh-salaries-table-sortable.responsive')
        for row in table.xpath('.//tr'):
            player_name = row.xpath('normalize-space(./td[@class="name"]/a/text())').get()
            value = row.xpath('./td[@class="value"]/text()').get().strip()
            href = row.xpath('./td[@class="name"]/a/@href').get()
            year = response.meta['year']

            player_record = self.collection.find_one({'player_name': player_name})
            if player_record:
                # Player exists, update the ratings
                ratings = player_record.get('ratings', [])
                if not any(rating['year'] == year for rating in ratings):
                # Year rating does not exist, add new rating
                    new_rating = Nba2kRatingItem(year=year, rating=value)
                    self.collection.update_one(
                        {'player_name': player_name},
                        {'$push': {'ratings': dict(new_rating)}}
                    )

                 # Check if 'player_headshot' is missing and href is available
                if not player_record.get('headshot_link') and href:
                    # No headshot, need to scrape it
                    player_item = PlayerItem(
                        player_name=player_name,
                        headshot_link="",  # Currently empty
                        href=href,
                        ratings=ratings  # Existing ratings
                    )
                    yield response.follow(href, self.parse_additional_info, meta={'item': player_item})
            else:
                # New player, create a new record
                ratings = [Nba2kRatingItem(year=year, rating=value)]
                player_item = PlayerItem(
                    player_name=player_name,
                    headshot_link="",  # Assume empty or fetch separately
                    ratings=ratings,
                    href=href
                )
                self.collection.insert_one(dict(player_item))

                # Follow the link for more data, if necessary
                if href:
                    yield response.follow(href, self.parse_additional_info, meta={'item': player_item})
                else:
                    yield player_item

    # def parse_additional_info(self, response):
    #     item = response.meta['item']

    #     # Extract the player headshot URL from the <div> with class "player-headshot"
    #     player_headshot = response.xpath('//div[@class="player-headshot"]/img/@src').get()
    #     if player_headshot:
    #         item['player_headshot'] = player_headshot

    #     yield item

    def parse_additional_info(self, response):
        item = response.meta['item']
        player_name = item['player_name']
        print(f'Parsing additional info for {player_name}')
        # Add additional parsing logic here, for example, to fetch a player's headshot link
        # Update the item and upsert into the database
        player_headshot = response.xpath('//div[@class="player-headshot"]/img/@src').get()
        print(f'Player headshot for {player_name} is {player_headshot}')
        if player_headshot:
            self.collection.update_one(
                {'player_name': player_name},
                {'$set': {'headshot_link': player_headshot}},
                upsert=True
            )
        yield item


    def close(self, reason):
        # Close the MongoDB connection when the spider is closed
        self.client.close()
