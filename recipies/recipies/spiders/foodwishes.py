import scrapy

# New Spider generated with $ scrapy genspider foodwishes foodwishes.blogspot.com
class FoodwishesSpider(scrapy.Spider):
    name = 'foodwishes'
    allowed_domains = ['foodwishes.blogspot.com']
    start_urls = ['http://foodwishes.blogspot.com/']

    def parse(self, response):
        # Get all the links from the main page pertaining to food
        links = response.css('div.BlogArchive a.post-count-link::attr(href)').getall()

        # Get all links from those resulting pages
        yield from response.follow_all(links, callback=self.parse_recipe_page)

    def parse_recipe_page(self, response):
        try:
            links = response.css('div.hfeed h3.entry-title a::attr(href)').getall()
        except Exception:
            links = response.css('div.entry-content h4 a::attr(href)').getall()

        yield from response.follow_all(links, callback=self.parse_recipe)

    def parse_recipe(self, response):

        for item in response.css('div.hentry'):
            yield {
                'title': item.css('h3.entry-title a::text').get().strip("\n"),
                'author' : 'Chef John',
                'tags' : item.css('span.post-labels a::text').getall(),       # getall() to return a list of tags
                'image': item.css('div.separator img::attr(src)').get(),
                'recipe_notes': item.css('span::text').get().strip("\n"),
                'url': str(response.url)
            }