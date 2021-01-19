import scrapy

class Food52(scrapy.Spider):
    name = 'food52' # identifies the spider to be run via terminal

    def start_requests(self):
        urls = [
            'https://food52.com/sitemap/recipes?page=1', # Page = 1, 2, 3, etc...
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('ul.content-listing a::attr(href)').getall() # Gether all recipe listing on page and send them to get parsed
        yield from response.follow_all(links, callback=self.parse_recipe) # Passes all of the links to parse_recipe


        next_page = response.css('div.pagination a.next_page::attr(href)').get() # Gather link to next page

        #Getting the next page via link and calling this function again
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_recipe(self, response): # Takes in a response object with the same properties, just a new URL.
        for item in response.css('div.content__container'): # Response should be the new page passed in.
            try:
                title = item.css('h1.recipe__title::text').get().strip().replace(u'\xa0', u' '),   # get() to get a single unique item
            except AttributeError:
                break

            yield {
                'title': title,
                'author' : item.css('div.meta__author a.meta__caps::text').get(),
                'tags' : item.css('ul.tag-list a.tag::text').getall(),       # getall() to return a list of tags
                'image': item.css('picture img::attr(data-pin-media)').get(),
                'recipe_notes': item.css('div.recipe__notes p').getall(),
                'url': str(response.url)
            }


        