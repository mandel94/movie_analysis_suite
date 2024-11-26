import scrapy
from ..items import MovieItem, ReviewItem  # Ensure these are defined


class RottenTomatoesMovieSpider(scrapy.Spider):
    name = "rotten_tomatoes_movie_spider"

    

    def __init__(self, query, parse_function, return_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.parse_function = parse_function
        self.return_list = return_list
        

    def start_requests(self):
        url = f'https://www.rottentomatoes.com/m/{self.query.replace(" ", "_")}'
        self.logger.info(f"Scraping {url}...")
        yield scrapy.Request(url=url, callback=getattr(self, self.parse_function))


    def parse_movie_details(self, response):
        movie = MovieItem()
        # Mocked data for demonstration
        movie['title'] = 'Reservoir Dogs'
        movie['year'] = 1992
        movie['rating'] = 'R'
        movie['genre'] = 'Crime'
        movie['director'] = 'Quentin Tarantino'
        movie['cast'] = ['Harvey Keitel', 'Tim Roth', 'Michael Madsen']
        movie['synopsis'] = 'After a simple jewelry heist goes terribly wrong, the surviving criminals begin to suspect that one of them is a police informant.'
        yield movie
        
        

    def parse_reviews(self, response):
        reviews = response.xpath('//xpath_to_reviews')
        for review in reviews:
            review_item = ReviewItem()
            review_item['author_name'] = review.xpath('.//author_name_xpath').get()
            review_item['comment'] = review.xpath('.//comment_xpath').get()
            # Additional review fields as necessary



