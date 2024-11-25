# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
<<<<<<< HEAD
import json
=======
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266


class MoviePipeline:
    def process_item(self, item, spider):
<<<<<<< HEAD
        return item
    

class SendToServer():
    "Send the item to a server for temporary storage"
    def open_spider(self):
        # Establish connection to the server
        raise NotImplementedError("This method must be implemented by the subclass")
    

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
=======
>>>>>>> bf90b263c6f2a54fb5634aa44b4cb178bbf64266
        return item