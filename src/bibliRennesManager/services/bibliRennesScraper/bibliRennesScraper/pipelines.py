# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from scrapy.exporters import JsonItemExporter

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


class BibliRennesJsonPipeline:

    cards_spiders = []

    exporter = []

    jsonFile = []

    def open_spider(self, spider):
        if not self.cards_spiders:
            self.jsonFile.append(open(f'items.json', 'wb'))
            self.exporter.append(JsonItemExporter(self.jsonFile[0], indent=4, encoding='utf8'))
            self.exporter[0].start_exporting()
        card = spider.cardId
        self.cards_spiders.append(card)

    def close_spider(self, spider):
        card = spider.cardId
        if card in self.cards_spiders:
            self.cards_spiders.remove(card)
        if not self.cards_spiders:
            self.exporter[0].finish_exporting()
            self.jsonFile[0].close()

    def process_item(self, item, spider):
        self.exporter[0].export_item(item)
        return item
