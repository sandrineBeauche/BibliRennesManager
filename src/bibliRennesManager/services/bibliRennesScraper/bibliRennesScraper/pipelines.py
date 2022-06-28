# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

class BiblirennesscraperPipeline:

    localisations = {}

    def process_item(self, item, spider):
        lst_ex = list(filter(lambda x: x.status == item.status, item.book.exemplaires))
        item.book.exemplaires = lst_ex
        item.deadline = datetime.strptime(item.status[7:15], "%d-%m-%y").date()
        if(len(lst_ex) > 0):
            ex = lst_ex[0]
            item.library = ex.localisation
            if not item.deadline in self.localisations:
                self.localisations[item.deadline] = item.library
        else:
            if item.deadline in self.localisations:
                item.library = self.localisations[item.deadline]
        return item
