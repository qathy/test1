import scrapy

class QuotesToscrape(scrapy.Spider):
    name = "quotes"
    allowed_domains = [u'toscrape.com']
    start_urls = [u'http://quotes.toscrape.com/random']
    
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        yield (
               'author_name': response.css('small.author::text').extract_first(),
               'text': response.css('span.text::text').extract_first(),
               'tags': response.css('a.tag::text').extract(),
              )
