<<<<<<< HEAD
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from rottentomatoes_scraper.rottentomatoes_scraper.spiders.RottenTomatoesSpiders import (
    RottenTomatoesMovieSpider,
)
from typing import List, Optional
from models import Movie, Review
from connections import TCPServer, TCPClient
import multiprocessing as mp
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from rottentomatoes_scraper.rottentomatoes_scraper.pipelines import (
    JsonWriterPipeline,
    MoviePipeline,
)
from scrapy.settings import Settings



def _start_crawl(_crawler_process, _crawler_settings, spider_cls, movie_name, parse_function, return_list):
    _crawler_process.settings = _crawler_settings
    _crawler_process.crawl(
        spider_cls,
        query=movie_name,
        parse_function=parse_function,
        return_list=return_list,
    )
    _crawler_process.start()


=======
from typing import List, Optional
from models import Movie, Review
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from twisted.internet.task import ensureDeferred
from rottentomatoes_scraper.rottentomatoes_scraper.spiders.RottenTomatoesSpiders import RottenTomatoesMovieSpider
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266

class RottenTomatoesService:
    """Service to fetch movie details and reviews from Rotten Tomatoes."""

    def __init__(self):
<<<<<<< HEAD
        self._scraper_settings = Settings()
        self._set_project_settings()
        self._crawler_process = CrawlerProcess()

    def _set_project_settings(self):
        self._scraper_settings.set(
            "ITEM_PIPELINES", {MoviePipeline: 300, JsonWriterPipeline: 400}
        )

    
    async def _start_crawl_wrapper(
        self, movie_name, parse_function
    ):
        return_list = []
        process = mp.Process(
            target=_start_crawl,
            args=(
                self._crawler_process,
                self._scraper_settings,
                RottenTomatoesMovieSpider,
                movie_name,
                parse_function,
                return_list,
            ),
        )
        process.start()
        process.join()
        return return_list

    async def get_movie(self, movie_name: str) -> Optional[Movie]:
        movie = await self._run_spider(movie_name, parse_function="parse_movie_details")
        return movie

    async def get_reviews(self, movie_name: str) -> List[Review]:
        raise NotImplementedError

    async def _run_spider(self, movie_name: str, parse_function: str):
        """Run the spider using CrawlerRunner and return extracted data."""
        movie = await self._start_crawl_wrapper(
            movie_name, parse_function
        )
        return movie
=======
        self.crawler_runner = CrawlerRunner()

    async def get_movie(self, movie_name: str) -> Optional[Movie]:
        return await self._run_spider(movie_name, parse_function="parse_movie_details")

    async def get_movie_reviews(self, movie_name: str) -> List[Review]:
        return await self._run_spider(movie_name, parse_function="parse_reviews")

    async def get_critics_movie_review(self, movie_name: str) -> List[Review]:
        all_reviews = await self.get_movie_reviews(movie_name)
        return [review for review in all_reviews if review.author.is_critic]

    async def _run_spider(self, movie_name: str, parse_function: str):
        """Run the spider using CrawlerRunner and return extracted data."""
        result_container = []

        @defer.inlineCallbacks
        def crawl():
            # Perform the crawl and return the extracted data
            data = yield self.crawler_runner.crawl(
                RottenTomatoesMovieSpider,
                query=movie_name,
                parse_function=parse_function,
            )
            defer.returnValue(data)  # Return the data extracted by the spider

        def on_crawl_success(data):
            """Callback to handle successful crawl."""
            result_container.append(data)
            return result_container  # Pass it forward for any further processing

        def on_crawl_failure(failure):
            """Callback to handle crawl failure."""
            print(f"Error during crawling: {failure}")
            return result_container  # Return the empty container if failed

        # Run the crawl and handle its completion via callbacks
        d = ensureDeferred(crawl())
        d.addCallback(on_crawl_success)
        d.addErrback(on_crawl_failure)

        # Wait for the deferred to complete and return the result
        await d
        return result_container
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
