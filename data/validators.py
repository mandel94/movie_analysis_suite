# Define collection schemas as JSON schema validators
validators = {
    "authors": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId"},
                "name": {"bsonType": "string", "description": "The name of the author of a movie"},
                "movies": {"bsonType": "array", "description": "The movies of an author"}
            }
        }
    },
    "cinemas": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId"},
                "tickets sold": {"bsonType": "int", "description": "Tickets sold count"},
                "city": {"bsonType": "string", "description": "City where the cinema is located"},
                "cinema": {"bsonType": "string", "description": "Name of the cinema"},
                "geo_data": {"bsonType": "object", "description": "The geospatial data of cinema"},
                "address": {"bsonType": "string", "description": "Address of the cinema"}
            }
        }
    },
    "consumers": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Universal privacy-preserving id representing a consumer"},
                "spent per capita": {"bsonType": "double", "description": "Amount spent per capita"},
                "audiences": {"bsonType": "array", "description": "Audiences associated with the consumer"}
            }
        }
    },
    "contents": {
        "$jsonSchema": {
            "bsonType": "object",
            "properties": {
                "reach": {"bsonType": "int", "description": "Content reach"}
            }
        }
    },
    "movies": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Universal movies id"},
                "penetration": {"bsonType": "double", "description": "Market penetration"},
                "attendance": {"bsonType": "int", "description": "Attendance count"},
                "revenue": {"bsonType": "double", "description": "Total revenue"},
                "author": {"bsonType": "string", "description": "Author of the movie"},
                "title": {"bsonType": "string", "description": "Title of the movie"}
            }
        }
    },
    "releases": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "ISO 8601 standard, used by Google Calendar"},
                "movies": {"bsonType": "array", "description": "List of movies to be released each day, each containing a movie_id"}
            }
        }
    },
    "reviews": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Unique ID for each review"},
                "comment": {"bsonType": "string", "description": "Review comment"},
                "stars": {"bsonType": "int", "description": "Star rating for the review"},
                "from_critic": {"bsonType": "bool", "description": "Indicates if the review is from a critic"}
            }
        }
    },
    "audiences": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id"],
            "properties": {
                "_id": {"bsonType": "objectId", "description": "Unique audience ID representing different spectator types"},
                "consumers": {"bsonType": "array", "description": "List of unique consumer IDs included in an audience"}
            }
        }
    }
}