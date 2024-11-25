import scrapy

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    synopsis = scrapy.Field()
    director = scrapy.Field()
    producers = scrapy.Field()
    distributor = scrapy.Field()
    genre = scrapy.Field()
    year = scrapy.Field()
    language = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()
    synopsis = scrapy.Field()
<<<<<<< HEAD
    rating = scrapy.Field()
    cast = scrapy.Field()
=======
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266


class ReviewItem(scrapy.Item):
    author_name = scrapy.Field()
    comment = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()