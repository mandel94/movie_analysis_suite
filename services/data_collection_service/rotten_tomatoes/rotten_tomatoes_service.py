from scrapy.crawler import CrawlerProcess
from rottentomatoes_scraper.rottentomatoes_scraper.spiders.RottenTomatoesSpiders import (
    RottenTomatoesMovieSpider,
)
from typing import List, Optional
from models import Movie, Review
import multiprocessing as mp
from rottentomatoes_scraper.rottentomatoes_scraper.pipelines import (
    JsonWriterPipeline,
    MoviePipeline,
)
from scrapy.settings import Settings
from connections import ClientConnectionParameters


def _start_crawl(
    _crawler_process,
    _crawler_settings,
    spider_cls,
    movie_name,
    parse_function,
    proxy_endpoint,
):
    _crawler_process.settings = _crawler_settings
    _crawler_process.crawl(spider_cls, query=movie_name, parse_function=parse_function, proxy_endpoint=proxy_endpoint)
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

    def _start_crawl_wrapper(self, movie_name, parse_function, proxy_endpoint):
        process = mp.Process(
            target=_start_crawl,
            args=(
                self._crawler_process,
                self._scraper_settings,
                RottenTomatoesMovieSpider,
                movie_name,
                parse_function,
                proxy_endpoint,
            ),
        )
        process.start()
        process.join()

    def get_movie(
        self, movie_name: str, proxy_endpoint: ClientConnectionParameters
    ) -> Optional[Movie]:
        self._run_spider(
            movie_name,
            parse_function="parse_movie_details",
            proxy_endpoint=proxy_endpoint,
        )
        # TODO Set client to wait for data

        # Return the movie data

    def get_reviews(self, movie_name: str) -> List[Review]:
        raise NotImplementedError

    def _run_spider(
        self,
        movie_name: str,
        parse_function: str,
        proxy_endpoint: ClientConnectionParameters,
    ):
        self._start_crawl_wrapper(movie_name, parse_function, proxy_endpoint)
