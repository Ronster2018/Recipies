import scrapy

# Extraced data from spiders -> Temporary Containers (items) -> Store to Database 

class RecipiesItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    image = scrapy.Field()
    recipe_notes = scrapy.Field()
    url = scrapy.Field()
    
