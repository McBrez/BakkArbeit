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
'''The class, which is called by the scrapy framework. '''
    name = 'ipspider'											# the name of the spider
    start_urls = ['https://opencores.org/projects?lang=0&stage=5&license=0&wishbone_version=0']		# the url where the scraping starts

    def parse(self, response):
        '''Default callback for scrapy. Starts at start_url, fetches the url of the different project pages, and calls parse_metadata for each project page'''
        for href in response.css('td.project a::attr(href)'):
            yield response.follow(href, self.parse_metadata)

    def parse_metadata(self, response):
	'''parses metadata of an opencore.org project page and returns a scrapy item object.'''
        def scrape_line(strArray,  removeStr):  
            '''helper function which iterates trough the string array 'strArray', selects the first entry which contains 'removeStr' and returns the string without removeStr and whitespaces.'''
            for str in strArray:
                if(str.find(removeStr) != -1):
                    retStr = str.replace(removeStr,  '')
                    return retStr.strip()
            
        def scrape_href(line):  
            '''helper function, which gets an html <a> element, checks if it has inner html and returns the text of the inner html'''
            start = line.find(">")
            end = line.find("<", start)
            if((start + 1) == end):
                return ""
            else:
                return line[(start+1):(end)]
            
        hdl_IP =  HDL_IP()
        hdl_IP['name'] = scrape_line(response.css('h2 + p::text').extract(), 'Name:')
        hdl_IP['created'] = scrape_line(response.css('h2 + p::text').extract(), 'Created:')
        hdl_IP['updated'] = scrape_line(response.css('h2 + p::text').extract(), 'Updated:')
        hdl_IP['downloadLink'] = 'https://opencores.org' + response.css('p a::attr(href)')[1].extract()
        hdl_IP['category'] = scrape_href(response.css('p a')[5].extract())
        hdl_IP['language'] = scrape_href(response.css('p a')[6].extract())
        hdl_IP['license'] = scrape_line(response.css('h2 + p::text').extract(),  'License:')
        
        yield hdl_IP
