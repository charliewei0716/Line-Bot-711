import abc

from . import store
from . import scrape

class Repository(abc.ABC):
    @abc.abstractmethod
    def _get_by_index(self) -> store.Store:
        raise NotImplementedError

    def __getitem__(self, index) -> store.Store:
        return self._get_by_index(index)

class InMemoryRepository(Repository):
    """ In-memory implementation of Repository. Feel free to use it in unit tests."""
    def __init__(self, store_scraper: scrape.StoreScraper):
        self.items = store_scraper.to_list()

    def _get_by_index(self, index)-> store.Store:
        return self.items[index]