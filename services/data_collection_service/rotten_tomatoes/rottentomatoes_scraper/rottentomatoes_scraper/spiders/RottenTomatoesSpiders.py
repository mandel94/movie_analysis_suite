import scrapy
import scrapy.signals
from ..items import MovieItem, ReviewItem  # Ensure these are defined
from connections import TCPClient
from itemadapter import ItemAdapter


class RottenTomatoesMovieSpider(scrapy.Spider):
    name = "rotten_tomatoes_movie_spider"

    def __init__(
        self,
        query: str,
        parse_function: str,
        client_of_proxy: TCPClient,
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
        self.client_of_proxy: TCPClient = client_of_proxy

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(RottenTomatoesMovieSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.send_to_server, signal=scrapy.signals.item_scraped)
        return spider

    def start_requests(self):
        """
        Initiate the scraping process by generating the initial request.
        """
        url: str = f'https://www.rottentomatoes.com/m/{self.query.replace(" ", "_")}'
        self.logger.info(f"Scraping {url}...")
        yield scrapy.Request(url=url, callback=getattr(self, self.parse_function))

    def parse_movie_details(self, response: scrapy.Response):
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

    def parse_reviews(self, response: scrapy.Response):
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

    def send_to_server(self, item) -> None:
        """
        Send data to the server using the storage client.

        :param data: The data to send, serialized as a dictionary.
        """
        self.client_of_proxy.send_as_json(ItemAdapter(item).asdict())
