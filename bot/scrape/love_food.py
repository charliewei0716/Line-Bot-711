from django.conf import settings
import requests
import json


lovefood_mid_v = settings.LOVEFOOD_MID_V

class LoveFoodScraper:
    token_url = f"https://lovefood.openpoint.com.tw/iMap/api/Auth/FrontendAuth/AccessToken?mid_v={lovefood_mid_v}"
    token_headers = {"User-Agent": "Chrome v22.2 Linux Ubuntu"}
    love_food_url = "https://lovefood.openpoint.com.tw/LoveFood/api/Search/FrontendStoreItemStock/GetStoreDetail"
    love_food_headers = {
        "User-Agent": "Chrome v22.2 Linux Ubuntu",
        "Content-Type": "application/json"
    }
    def __init__(self, store) -> None:
        self._store = store
        self._token = self._get_token()
        self._stock_item, self._update_time, self._n_stock_item = self._get_love_food_info()

    @property
    def stock_item(self):
        return self._stock_item

    @property
    def update_time(self):
        return self._update_time

    @property
    def n_stock_item(self):
        return self._n_stock_item

    def _get_token(self):
        return requests.post(self.token_url, headers=self.token_headers).json()["element"]

    def _get_love_food_info(self):
        params = {"token": self._token}
        data = {
            "CurrentLocation": {
                "Latitude": 24, "Longitude": 120
            },
            "StoreNo": self._store.POI_id
        }
        response = requests.post(
            "https://lovefood.openpoint.com.tw/LoveFood/api/Search/FrontendStoreItemStock/GetStoreDetail",
            headers=self.love_food_headers,
            data=json.dumps(data),
            params=params
        ).json()

        stock_item = response["element"]["StoreStockItem"]["CategoryStockItems"]
        update_time = response["element"]["StoreItemStockUpdateTime"]
        n_stock_item = len(stock_item)

        return stock_item, update_time, n_stock_item

