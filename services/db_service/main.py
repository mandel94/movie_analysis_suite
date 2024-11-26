# This files triggers the data collection process


# It needs a list of movies to collect data for

# It needs to collect data for each movie in the list, collecting data from 
# different sources, standardizing the data, and storing it in a database.

import json
from typing import Any, TypeAlias, Union
from dataclasses import dataclass

DB_URL = "mongodb://localhost:27017/"

# Define data structure for movie
@dataclass
class MovieDType:
    title: str

PathDType: TypeAlias = Union[str]


def _get_list_of_movies_from_json_file(source: str) -> list[MovieDType]:
    with open(source, "r") as f:
        file_with_movies = json.load(f)
    return file_with_movies["list"]


def get_list_of_movies(source: PathDType) -> list[MovieDType]:
    return _get_list_of_movies_from_json_file(source)
        




if __name__ == "__main__":
    movie_list_dict = get_list_of_movies(source="user_fed_movie_list.json")
    






