import scrapy

class QuotesToscrape(scrapy.Spider):
    name = "all_tags"
    allowed_domains = [u'toscrape.com']
    start_urls = [u'http://quotes.toscrape.com/']
    all_tags = {}
    
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        quotes = response.css('div.quote')
        # manage page tag if we are on a page tag
        tag_head = response.css('h3 > a::text').extract_first()
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if tag_head:
            tag = self.all_tags[tag_head]
            tag['visited'] = True
            tag['#quotes'] = tag['#quotes'] + quotes.count()
            if not next_page_url:
                yield tag
                sample = quotes[0]
                yield {
                       'author_name': sample.css('small.author::text').extract_first(),
                       'text': sample.css('span.text::text').extract_first(),
                      }
        # collect tags from any visited page
        for quote in quotes:
            tags = quote.css('a.tag')
            for tag in tags:
                tag_text = tag.css('a::text').extract_first()
                if not tag_text in self.all_tags:
                    self.all_tags[tag_text] = {
                                          'url': tag.css('a::attr(href)').extract_first(),
                                          'visited': False,
                                          '#quotes': 0,
                                         }
        # visit one unvisited tag page
        for tag in self.all_tags.itervalues():
            if not tag['visited']:
                next_tag_url = response.urljoin(tag['url'])
                yield scrapy.Request(url=next_tag_url, callback=self.parse)
                break
        # visit next page if there's a next button
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
