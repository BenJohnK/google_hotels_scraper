# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleHotelScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hotel_name = scrapy.Field()
    check_in = scrapy.Field()
    check_out = scrapy.Field()
    price = scrapy.Field()
    data_id = scrapy.Field()
    official_site_div_content = scrapy.Field()
    input_hotel_name = scrapy.Field()

