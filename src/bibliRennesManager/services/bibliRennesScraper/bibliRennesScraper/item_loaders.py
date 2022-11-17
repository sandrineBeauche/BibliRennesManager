from . import processors
from itemloaders.processors import Identity, TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader


class BibliRennesLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if "response" in kwargs:
            self.response = kwargs["response"]


class BookLoader(BibliRennesLoader):
    title_in = MapCompose(processors.extract_title, str.strip)
    
    authors_in = MapCompose(processors.extract_author, str.strip)
    authors_out = Join(separator=" - ")

    exemplaires_in = Identity()
    exemplaires_out = Identity()

    notes_out = Join(separator=", ")

    cover_in = Identity()
    cover_out = TakeFirst()

    def add_details_values(self, label, link, field):
        
        def get_details_values(label, link=False):
            elts = self.response.xpath("//td[normalize-space() = '" + label + "']") 
            if link:
                pattern = "../td[2]/div/a/text()"
            else:
                pattern = "../td[2]/div/text()"
            result = [c.get() for current in elts for c in current.xpath(pattern)]
            return result    
        
        for value in get_details_values(label, link):
            if value != '':
                self.add_value(field, value)

    
class ExemplaireLoader(BibliRennesLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()


class LoanItemLoader(BibliRennesLoader):
    status_in = MapCompose(processors.stripAll)

    deadline_in = MapCompose(str.strip, processors.extract_deadline)
    renewed_in = Identity()
    renewed_out = processors.BooleanOr()
    reservation_in = Identity()
    reservation_out = processors.BooleanOr()

    book_in = Identity()

