import scrapy

class QuotesToscrape(scrapy.Spider):
    name = "quotes"
    allowed_domains = [u'toscrape.com']
    start_urls = [u'http://quotes.toscrape.com/']
    
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for quote in response.css('div.quote'):
            item = {
               'author_name': quote.css('small.author::text').extract_first(),
               'text': quote.css('span.text::text').extract_first(),
               'tags': quote.css('a.tag::text').extract(),
              }
            yield item
