import scrapy

class QuotesToscrape(scrapy.Spider):
    name = "all_tags"
    allowed_domains = [u'toscrape.com']
    start_urls = [u'http://quotes.toscrape.com/']
    all_tags = {}
    all_quotes = set()
    
    def parse(self, response):
        self.log('I just visited: ' + response.url)
        quotes = response.css('div.quote')
        # manage page tag if we are on a page tag
        tag_head = response.css('h3 > a::text').extract_first()
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if tag_head:
            tag = self.all_tags[tag_head]
            tag['visited'] += 1
            tag['#quotes'] += len(quotes)
            if 'author_sample' not in tag:
                for sample in quotes:
                    qt = sample.css('span.text::text').extract_first()
                    if qt not in self.all_quotes:
                        self.all_quotes.add(qt)
                        tag['author_sample'] = sample.css('small.author::text').extract_first()
                        tag['text_sample'] = qt
            if not next_page_url: # wait to reach last page for the tag before sending the item
                yield tag
        # collect tags from any visited page
        for quote in quotes:
            tags = quote.css('a.tag')
            for tag in tags:
                tag_text = tag.css('a::text').extract_first()
                if not tag_text in self.all_tags:
                    self.all_tags[tag_text] = {
                                          'url': response.urljoin(tag.css('a::attr(href)').extract_first()),
                                          'visited': 0,
                                          '#quotes': 0,
                                         }
        # visit one unvisited tag page
        for tag in self.all_tags.values():  # to avoid runtime error if tags are added during the loop
            if not tag['visited']:
                next_tag_url = tag['url']
                yield scrapy.Request(url=next_tag_url, callback=self.parse)
                # break commenting this line may lead to visit several times each tag page
        # visit next page if there's a next button
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
