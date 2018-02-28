import scrapy
#from ipspider.items import  IpspiderItem

class HDL_IP(scrapy.Item):
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
        '''walks trough the different projects and calls parse_metadata for each project'''
        for href in response.css('td.project a::attr(href)'):
            yield response.follow(href, self.parse_metadata)

    def parse_metadata(self, response):
        def scrape_line(line,  removeStr):  
            '''helper function which removes removeStr from line and strips all trailing and leading whitespaces'''
            retStr = line.replace(removeStr, '')
            return retStr.strip()
            
        def scrape_href(line):  
            '''gets an html <a> element, checks if it has inner html and returns the text of the inner html'''
            start = line.find(">")
            end = line.find("<", start)
            if((start + 1) == end):
                return ""
            else:
                return line[(start+1):(end)]
            
        hdl_IP =  HDL_IP()
        hdl_IP['name'] = scrape_line(response.css('h2 + p::text')[0].extract(), 'Name:')
        hdl_IP['created'] = scrape_line(response.css('h2 + p::text')[1].extract(), 'Created:')
        hdl_IP['updated'] = scrape_line(response.css('h2 + p::text')[2].extract(), 'Updated:')
        hdl_IP['downloadLink'] = 'https://opencores.org' + response.css('p a::attr(href)')[1].extract()
        hdl_IP['category'] = scrape_href(response.css('p a')[5].extract())
        hdl_IP['language'] = scrape_href(response.css('p a')[6].extract())
        hdl_IP['license'] = scrape_line(response.css('h2 + p::text')[17].extract(),  'License:')
        
        yield hdl_IP
