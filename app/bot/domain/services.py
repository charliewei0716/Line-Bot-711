from . import scrape
from . import model


class InvalidKeyWord(Exception):
    pass


def is_invalid_key_word(store_scraper: scrape.StoreScraper):
    return len(store_scraper) == 0


def to_flex(key_word: str):
    #
    store_scraper = scrape.StoreScraper(key_word)
    if is_invalid_key_word(store_scraper):
        raise InvalidKeyWord
    list_store = store_scraper.to_list()
    #
    store_scraper = scrape.LoveFoodScraper(list_store[0])
    list_category_stock_item = store_scraper.to_list()
    #
    flex = model.to_flex(
        list_store,
        list_category_stock_item,
        store_scraper.update_time,
        key_word
    )
    return flex
