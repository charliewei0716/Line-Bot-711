import requests
from typing import List
from dataclasses import dataclass, field
from urllib import parse
from bs4 import BeautifulSoup


@dataclass
class Store:
    POI_id: str
    POI_name: str
    tel_no: str
    fax_no: str
    address: str
    service: List[str]
    google_map_url: str = field(init=False)
    tel_no_url: str = field(init=False)
    service_no: List[str] = field(init=False)

    def __post_init__(self):
        google_map_query = parse.quote("7-ELEVEN " + self.POI_name + "門市")
        google_map_search_url = "https://www.google.com/maps/search/?api=1&query="
        self.google_map_url = google_map_search_url + google_map_query
        self.tel_no_url = "tel:" + self.tel_no
        self.service_no = [service[:2] for service in self.service]


class WebScraper:
    url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def __init__(self, store_name: str) -> None:
        self._store_name = store_name
        self._soup = self.scrape()

    @property
    def store_name(self):
        return self._store_name

    @property
    def soup(self):
        return self._soup
        
    def scrape(self):
        requests_data = parse.urlencode(
            {
                "commandid": "SearchStore",
                "city": "",
                "town": "",
                "roadname": "",
                "ID": "",
                "StoreName": self._store_name,
                "SpecialStore_Kind": "",
                "leftMenuChecked": "",
                "address": "",
            }
        )

        xml = requests.post(
            self.url, headers=self.headers, data=requests_data
        )

        return BeautifulSoup(xml.text, "xml")



class StoreScraper:
    def __init__(self, soup: BeautifulSoup) -> None:
        self._soup = soup
        self._n_store = self._count_store()

    @property
    def n_store(self):
        return self._n_store
    
    def _count_store(self) -> int:
        return len(self._soup.find_all("POIID"))

    def _get_element(self, key_word, index) -> str:
        element_str = self._soup.find_all(key_word)[index].get_text().strip()
        return element_str or " "

    def _get_store(self, index) -> Store:
        POI_id = self._get_element("POIID", index)
        POI_name = self._get_element("POIName", index)
        tel_no = self._get_element("Telno", index)
        fax_no = self._get_element("FaxNo", index)
        address = self._get_element("Address", index)
        service = self._get_element("StoreImageTitle", index).split(",")
        return Store(POI_id, POI_name, tel_no, fax_no, address, service)

    def main_store(self) -> Store:
        return self._get_store(0)

    def other_store(self) -> List[Store]:
        if self._n_store <= 1:
            return []
        else:
            return [self._get_store(index) for index in range(1, self._n_store)]