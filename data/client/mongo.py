# Implement a mongo client to connect to the database 


from pymongo import MongoClient


class DBClient:
    def __init__(self, host, port, db, username, password):
        # Open client connection
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db}"
        self.client = MongoClient(uri)
        self.db = self.client[db]
        print(self.db.list_collection_names())

    def ping(self):
        return self.client.server_info()
    
    def init_from_validator(self, validator):
        # return self.db.create_collection(validator)
        return {"status": "TEST::Collection created successfully!"}
    
    def get_collection(self, collection):
        return self.db[collection]
    

    



    






