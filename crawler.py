import scrapy


class LtnSearchCrawler(scrapy.Spider):
    name = 'ltn_search_page'
    start_urls = ['https://news.ltn.com.tw/search/?keyword=反紅媒']

    def parse(self, response):
        for block in response.xpath('//ul[@id="newslistul"]//li'):
            href = block.xpath('.//a[contains(@class, "tit")]/@href').extract_first()
            yield response.follow(url=href, callback=self.parse_content)
        a_next = response.xpath('//a[contains(@class, "p_next")]/@href').extract_first()
        if a_next:
            yield response.follow(a_next, callback=self.parse)

    def parse_content(self, response):
        for body in response.xpath('//div[contains(@class, "articlebody")]'):
            title = body.xpath('./h1/text()').get()
            view_time = body.xpath('.//span[contains(@class, "viewtime")]/text()').get()
            contents = body.xpath('.//div[contains(@class, "text")]//p//text()').extract()
            content = ' '.join(contents)
            if len(content) > 300:
                content = content[:300]
            if response.url and title and view_time and content:
                yield {
                    'url': response.url,
                    'title': title,
                    'date': view_time,
                    'content': content,
                }
