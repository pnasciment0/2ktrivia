import scrapy

class NbaTriviaItem(scrapy.Item):
    # Represents a single game's rating for a player
    year = scrapy.Field()
    value = scrapy.Field()
    player_name = scrapy.Field()
    player_headshot = scrapy.Field()
    href = scrapy.Field()

class Nba2kRatingItem(scrapy.Item):
    # Represents a single game's rating for a player
    year = scrapy.Field()
    rating = scrapy.Field()

class PlayerItem(scrapy.Item):
    # Represents a player, including their name, headshot link, and a list of their ratings across different NBA 2K games
    player_name = scrapy.Field()
    headshot_link = scrapy.Field()
    href = scrapy.Field()
    ratings = scrapy.Field(serializer=list)
