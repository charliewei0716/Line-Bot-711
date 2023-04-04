import requests
import json
from urllib import parse
from bs4 import BeautifulSoup
from decouple import config

from . import store


class StoreScraper:
    url = "https://emap.pcsc.com.tw/EMapSDK.aspx"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def __init__(self, key_word: str) -> None:
        self._key_word = key_word
        self._soup = self._scrape()
        self._n_store = self._count_store()

    def __len__(self):
        return self._n_store

    def _scrape(self) -> BeautifulSoup:
        requests_data = parse.urlencode(
            {
                "commandid": "SearchStore",
                "city": "",
                "town": "",
                "roadname": "",
                "ID": "",
                "StoreName": self._key_word,
                "SpecialStore_Kind": "",
                "leftMenuChecked": "",
                "address": "",
            }
        )

        xml = requests.post(
            self.url, headers=self.headers, data=requests_data
        )

        return BeautifulSoup(xml.text, "xml")

    def _count_store(self) -> int:
        return len(self._soup.find_all("POIID"))

    def _get_element(self, element, index: int) -> str:
        element_str = self._soup.find_all(element)[index].get_text().strip()
        return element_str or " "

    def _get_store(self, index) -> store.Store:
        poi_id = self._get_element("POIID", index)
        poi_name = self._get_element("POIName", index)
        tel_no = self._get_element("Telno", index)
        fax_no = self._get_element("FaxNo", index)
        address = self._get_element("Address", index)
        service = self._get_element("StoreImageTitle", index).split(",")
        service = [_[:2] for _ in service]
        return store.Store(poi_id, poi_name, tel_no, fax_no, address, service)

    def to_list(self):
        return [self._get_store(index) for index in range(self._n_store)]


class LoveFoodScraper:
    lovefood_mid_v = config("LOVEFOOD_MID_V")
    token_url = f"https://lovefood.openpoint.com.tw/iMap/api/Auth/FrontendAuth/AccessToken?mid_v={lovefood_mid_v}"  # noqa
    token_headers = {"User-Agent": "Chrome v22.2 Linux Ubuntu"}
    love_food_url = "https://lovefood.openpoint.com.tw/LoveFood/api/Search/FrontendStoreItemStock/GetStoreDetail"  # noqa
    love_food_headers = {
        "User-Agent": "Chrome v22.2 Linux Ubuntu",
        "Content-Type": "application/json"
    }

    def __init__(self, store: store.Store) -> None:
        self._store = store
        self._token = self._get_token()
        self._dict_stock_item, self._update_time = self._get_love_food_info()

    @property
    def update_time(self) -> str:
        return self._update_time

    def _get_token(self):
        return requests.post(
            self.token_url, headers=self.token_headers
        ).json()["element"]

    def _get_love_food_info(self):
        params = {"token": self._token}
        data = {
            "CurrentLocation": {
                "Latitude": 24, "Longitude": 120
            },
            "StoreNo": self._store.poi_id
        }
        response = requests.post(
            "https://lovefood.openpoint.com.tw/LoveFood/api/Search/FrontendStoreItemStock/GetStoreDetail",  # noqa
            headers=self.love_food_headers,
            data=json.dumps(data),
            params=params
        ).json()

        dict_stock_item = response["element"]["StoreStockItem"]["CategoryStockItems"]   # noqa
        update_time = response["element"]["StoreItemStockUpdateTime"]

        return dict_stock_item, update_time

    def _to_list_stock_item(self, item_list):
        list_item = []
        for stock_item in item_list:
            list_item.append(
                store.StockItem(
                    stock_item["ItemName"],
                    stock_item["RemainingQty"]
                )
            )
        return list_item

    def to_list(self):
        list_category_stock_item = []
        for category_stock_item in self._dict_stock_item:
            name = category_stock_item["Name"]
            list_item = self._to_list_stock_item(
                category_stock_item["ItemList"]
            )
            list_category_stock_item.append(
                store.CategoryStockItem(name, list_item)
            )
        return list_category_stock_item
