from ..bibliRennesScraper import processors 
from itemloaders.processors import Identity, TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader

class BibliRennesLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()



class BookLoader(BibliRennesLoader):
    title_in = MapCompose(processors.extract_title, str.strip)
    
    authors_in = MapCompose(processors.extract_author, str.strip)
    authors_out = Join(separator=", ")

    exemplaires_in = Identity()
    exemplaires_out = Identity()

    notes_out = Join(separator=", ")

    
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

