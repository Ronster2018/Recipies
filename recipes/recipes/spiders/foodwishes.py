import scrapy
from ..items import RecipesItem

# New Spider generated with $ scrapy genspider foodwishes foodwishes.blogspot.com
class FoodwishesSpider(scrapy.Spider):
    name = 'foodwishes'
    allowed_domains = ['foodwishes.blogspot.com']
    start_urls = ['http://foodwishes.blogspot.com/']

    def parse(self, response):
        # Get all the links from the main page pertaining to food
        links = response.css('div.BlogArchive a.post-count-link::attr(href)').getall()

        # Get all links from those resulting pages
        yield from response.follow_all(links, callback=self.parse_recipes_page)

    def parse_recipes_page(self, response):
        try:
            links = response.css('div.hfeed h3.entry-title a::attr(href)').getall()
        except Exception:
            links = response.css('div.entry-content h4 a::attr(href)').getall()

        yield from response.follow_all(links, callback=self.parse_recipes)

    def parse_recipes(self, response):
        container = RecipesItem()
        for item in response.css('div.hentry'):

            container['title'] = item.css('h3.entry-title a::text').get().strip("\n")
            container['author'] = 'Chef John'
            container['tags'] =  item.css('span.post-labels a::text').getall()
            container['image'] = item.css('div.separator img::attr(src)').get()
            container['recipe_notes'] = item.css('span::text').get().strip("\n")
            container['url'] = response.url
            
            # yield {
            #     'title': item.css('h3.entry-title a::text').get().strip("\n"),
            #     'author' : 'Chef John',
            #     'tags' : item.css('span.post-labels a::text').getall(),       # getall() to return a list of tags
            #     'image': item.css('div.separator img::attr(src)').get(),
            #     'recipe_notes': item.css('span::text').get().strip("\n"),
            #     'url': str(response.url)
            # }

            yield container