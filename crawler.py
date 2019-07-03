import scrapy


class LtnSearchCrawler(scrapy.Spider):

    base_url = 'https://news.ltn.com.tw/'
    name = 'ltn_search_page'
    start_urls = ['https://news.ltn.com.tw/search/?keyword=反紅媒']

    def parse(self, response):
        for block in response.xpath('//ul[@id="newslistul"]//li'):
            href = block.xpath('.//a[contains(@class, "tit")]/@href').get()
            content_url = '{base_url}{href}'.format(base_url=self.base_url, href=href)
            yield scrapy.Request(url=content_url, callback=self.parse_content)

    def parse_content(self, response):
        for body in response.xpath('//div[contains(@class, "articlebody")]'):
            title = body.xpath('./h1/text()').get()
            view_time = body.xpath('.//span[contains(@class, "viewtime")]/text()').get()
            contents = body.xpath('.//div[contains(@class, "text")]//p//text()').extract()
            content = ' '.join(contents)
            if len(content) > 300:
                content = content[:300]
            yield {
                'url': response.url,
                'title': title,
                'date': view_time,
                'content': content,
            }
