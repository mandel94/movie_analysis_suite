# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class MoviePipeline:
    def process_item(self, item, spider):
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
        return item