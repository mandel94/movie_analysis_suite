import scrapy
from scrapy.http import Response, Request
from typing import Callable
from ..items import MovieItem, ReviewItem  # Ensure these are defined
from connections import TCPClient


class RottenTomatoesMovieSpider(scrapy.Spider):
    name = "rotten_tomatoes_movie_spider"

    def __init__(
        self,
        query: str,
        parse_function: str,
        storage_client: TCPClient,
        *args,
        **kwargs,
    ) -> None:
        """
        Initialize the spider.

        :param query: The movie query string.
        :param parse_function: The name of the function to parse the response.
        :param storage_client: An instance of a TCP client for data storage.
        """
        super().__init__(*args, **kwargs)
        self.query: str = query
        self.parse_function: str = parse_function
        self.storage_client: TCPClient = storage_client

    def start_requests(self) -> Request:
        """
        Initiate the scraping process by generating the initial request.
        """
        url: str = f'https://www.rottentomatoes.com/m/{self.query.replace(" ", "_")}'
        self.logger.info(f"Scraping {url}...")
        yield scrapy.Request(url=url, callback=getattr(self, self.parse_function))

    def parse_movie_details(self, response: Response) -> MovieItem:
        """
        Parse movie details from the response.

        :param response: The HTTP response object.
        :return: A populated MovieItem.
        """
        movie = MovieItem()
        # Mocked data for demonstration
        movie["title"] = "Reservoir Dogs"
        movie["year"] = 1992
        movie["rating"] = "R"
        movie["genre"] = "Crime"
        movie["director"] = "Quentin Tarantino"
        movie["cast"] = ["Harvey Keitel", "Tim Roth", "Michael Madsen"]
        movie["synopsis"] = (
            "After a simple jewelry heist goes terribly wrong, the surviving criminals begin to suspect that one of them is a police informant."
        )
        yield movie

    def parse_reviews(self, response: Response) -> ReviewItem:
        """
        Parse reviews from the response.

        :param response: The HTTP response object.
        :return: A populated ReviewItem for each review found.
        """
        reviews = response.xpath("//xpath_to_reviews")
        for review in reviews:
            review_item = ReviewItem()
            review_item["author_name"] = review.xpath(".//author_name_xpath").get()
            review_item["comment"] = review.xpath(".//comment_xpath").get()
            # Additional review fields as necessary
            yield review_item

    def send_to_server(self, data: dict) -> None:
        """
        Send data to the server using the storage client.

        :param data: The data to send, serialized as a dictionary.
        """
        self.storage_client.send_data_as_json(data)
