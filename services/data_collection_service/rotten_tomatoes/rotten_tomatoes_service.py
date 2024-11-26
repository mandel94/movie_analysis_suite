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



class RottenTomatoesService:
    """Service to fetch movie details and reviews from Rotten Tomatoes."""

    def __init__(self):
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
