# -*- coding: utf-8 -*-
import scrapy.http.Request
import scrapy.Spider

class IcharityInSpider(scrapy.Spider):
    name = 'icharity_in'
    allowed_domains = ['www.icharity.in']
    start_urls = ['http://www.icharity.in/ngos/ngo-list.html#']

    def parse(self, response):
        for al in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            url=response.url+al
            yield Request(url, self.parse_page)

    def parse_page(self,response):
        ngos=response.css(".ngo-list>li>a")
        for ngo in ngos:
            name=ngo.xpath("./@title").extract_first()
            link=ngo.xpath("./@href").extract_first()
            yield Request(link, self.ngo_scrape, meta={ "name": name})

    def ngo_scrape(self, response):
        name=response.meta['name']
        content=response.css("div.content")
        description=content[0].xpath("./p/span/text()").extract()
        description="\n".join(description)
        contact=content[-1].xpath("./p/*/text()").extract()
        phone=contact[-1]+" " + contact[-2]
        email=contact[-3]
        state=contact[5]
        cause_areas=response.css("div#subitems-128>div>ul>li.si-menuitem>a::text").extract()
        ret={"name":name,
        "description":description,
        "phone": phone,
        "email": email,
        "cause_areas": "/".join(cause_areas)
        }
        return(ret)





