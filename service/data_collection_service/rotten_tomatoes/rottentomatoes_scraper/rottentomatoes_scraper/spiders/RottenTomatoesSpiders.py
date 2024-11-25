import scrapy
<<<<<<< HEAD
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


=======
from scrapy.crawler import CrawlerRunner
from ..items import MovieItem, ReviewItem  # Ensure these are defined

class RottenTomatoesMovieSpider(scrapy.Spider):
    name = "rotten_tomatoes_movie_spider"

    def __init__(self, query, parse_function, result_container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.parse_function = parse_function
        self.result_container = result_container

    def start_requests(self):
        url = f'https://www.rottentomatoes.com/m/{self.query.replace(" ", "_")}'
        yield scrapy.Request(url=url, callback=getattr(self, self.parse_function))

>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
    def parse_movie_details(self, response):
        movie = MovieItem()
        # Mocked data for demonstration
        movie['title'] = 'Reservoir Dogs'
        movie['year'] = 1992
        movie['rating'] = 'R'
<<<<<<< HEAD
        movie['genre'] = 'Crime'
        movie['director'] = 'Quentin Tarantino'
        movie['cast'] = ['Harvey Keitel', 'Tim Roth', 'Michael Madsen']
        movie['synopsis'] = 'After a simple jewelry heist goes terribly wrong, the surviving criminals begin to suspect that one of them is a police informant.'
        yield movie
        
        
=======
        # Add more fields as necessary
        self.result_container.append("New movie")
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266

    def parse_reviews(self, response):
        reviews = response.xpath('//xpath_to_reviews')
        for review in reviews:
            review_item = ReviewItem()
            review_item['author_name'] = review.xpath('.//author_name_xpath').get()
            review_item['comment'] = review.xpath('.//comment_xpath').get()
            # Additional review fields as necessary

<<<<<<< HEAD


=======
            self.result_container.append(review_item)
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
