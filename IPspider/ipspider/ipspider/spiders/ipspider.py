import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    downloadLink = scrapy.Field()
    category = scrapy.Field()
    language = scrapy.Field()
    license = scrapy.Field()


class IPspider(scrapy.Spider):
    name = 'ipspider'

    start_urls = ['https://opencores.org/projects?lang=0&stage=5&license=0&wishbone_version=0']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('td.project a::attr(href)'):
            yield response.follow(href, self.parse_metadata)

    def parse_metadata(self, response):
        yield {
            'details': response.css('div.content p::text').extract()
        }
