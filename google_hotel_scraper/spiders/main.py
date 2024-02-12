import scrapy
import csv
import os
from urllib.parse import urlencode
from lxml.html import fromstring
from html import unescape
from ordered_set import OrderedSet
from google_hotel_scraper.items import GoogleHotelScraperItem


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["example.com", "www.google.com"]
    start_urls = ["https://example.com"]
    custom_settings = {
		'FEEDS': { 'output.csv': { 'format': 'csv', 'overwrite': True}},
        'FEED_EXPORT_FIELDS': [
            'hotel_name',
            'check_in',
            'check_out',
            'price',
            'data_id',
            'official_site_div_content',
            'input_hotel_name'
        ]
	}

    def parse(self, response):
        url_reader = list(csv.DictReader(open(os.path.join(os.path.dirname('__file__'), 'input_hotel_names.csv'))))
        for item in url_reader:
            input_hotel_name = item.get("input_hotel_name")
            meta = {
                "input_hotel_name": input_hotel_name,
            }
            headers = {
                'authority': 'www.google.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"121.0.6167.139"',
                'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.139", "Chromium";v="121.0.6167.139"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Linux"',
                'sec-ch-ua-platform-version': '"5.19.0"',
                'sec-ch-ua-wow64': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            params = {
                "q": input_hotel_name,
            }
            url = f"https://www.google.com/travel/search?{urlencode(params)}"
            yield scrapy.Request(url, headers=headers, meta=meta, callback=self.parse_hotel_page)

    def parse_hotel_page(self, response):
        meta = response.meta
        input_hotel_name = meta["input_hotel_name"]
        parser = fromstring(response.text)
        all_options_official_divs=parser.xpath("//div/h2[contains(text(), 'All options')]/following::div[1][@jsshadow and @jscontroller and @jsname and @class]//div[@data-id and descendant::span[contains(text(), 'Official Site')]]")
        all_options_official_div = all_options_official_divs[0] if all_options_official_divs else None
        if all_options_official_div:
            text_content_list = all_options_official_div.xpath(".//text()")
            div_id = all_options_official_div.xpath("./@data-id")
            text_content_list = list(map(lambda x: self.clean_text(x), text_content_list))
            text_content_list = list(filter(None, text_content_list))
            text_content_list = list(OrderedSet(text_content_list))
            hotel_name = text_content_list[0]
            price = None
            for text_content in text_content_list:
                if text_content.startswith("₹"):
                    price = text_content
                    break
            check_in_date = parser.xpath("//input[@type='text' and @placeholder='Check-in']/@value")
            check_out_date = parser.xpath("//input[@type='text' and @placeholder='Check-out']/@value")
            official_site_div_content = "-".join(text_content_list)
            data = {
                "hotel_name": hotel_name,
                "check_in": check_in_date[0] if check_in_date else None,
                "check_out": check_out_date[0] if check_out_date else None,
                "price": price,
                "data_id": div_id[0],
                "official_site_div_content": official_site_div_content,
                "input_hotel_name": input_hotel_name
            }
            yield GoogleHotelScraperItem(**data)

    def clean_text(self, text):
        if not text or not str(text).strip():
            return
        return ' '.join(unescape(text).split()).strip()
