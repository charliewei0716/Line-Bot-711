import abc
import os
from datetime import datetime
from typing import List, Dict
from urllib import parse
from decouple import config

from . import store


def to_flex(
    list_store: List[store.Store],
    list_category_stock_item: List[store.CategoryStockItem],
    updata_time: str,
    key_word: str
):
    store = list_store[0]
    carousel = get_store_carousel(store)
    for sub_list_item in sub_list(list_category_stock_item, 5):
        carousel += get_love_food_carousel(store, sub_list_item, updata_time)
    if has_other_carousel(list_store):
        other_carousel = get_other_carousel(list_store, key_word)
        carousel += other_carousel
    return carousel.flex


def get_store_carousel(store: store.Store):
    store_bubble = StoreBubble(store)
    return Carousel(store_bubble)


def sub_list(main_list: List, num: int):
    return [main_list[start:start+num] for start in range(0, len(main_list), num)]


def get_love_food_carousel(
    store: store.Store,
    list_category_stock_item: List[store.CategoryStockItem],
    update_time: str
):
    love_food_bubble = LoveFoodBubble(store, list_category_stock_item, update_time)
    return Carousel(love_food_bubble)


def has_other_carousel(list_store: List[store.Store]):
    return len(list_store) > 1


def get_other_carousel(list_store: List[store.Store], key_word:str):
    other_bubble = None
    for store in list_store[1:]:
        temp_other_bubble = OtherBubble(store, key_word, len(list_store))
        temp_other_bubble.create_body_contents()
        if other_bubble:
            other_bubble += temp_other_bubble
        else:
            other_bubble = temp_other_bubble
    return Carousel(other_bubble)


class Bubble(abc.ABC):
    @property
    @abc.abstractmethod
    def flex(self) -> Dict:
        raise NotImplementedError


class Carousel:
    def __init__(self, bubble: Bubble) -> None:
        self.contents = [bubble.flex]
    
    def __add__(self, other: object) -> object:
        self.contents += other.contents
        return self

    @property
    def flex(self) -> Dict:
        return {
            "type": "carousel", "contents": self.contents
        }


class StoreBubble(Bubble):
    line_liff_url = config("LINE_LIFF_URL")
    google_map_search_url = "https://www.google.com/maps/search/?api=1&query="
    store_image_url = "https://drive.google.com/uc?export=view&id=1bh8pHsrrbFhtPb57CAO8-l0CzSjlo_5m"

    def __init__(self, store: store.Store):
        self._store = store

    def _get_service_flex(self, num: int) -> List:
        flex = []
        for row_start in range(0, len(self._store.service), num):
            box_contents = []
            row = self._store.service[row_start: row_start+num]

            for store_service in row:
                icon_url = f"https://emap.pcsc.com.tw/menuImg/service_{store_service}.jpg"
                icon = {
                    "type": "icon", "size": "xxl", "url": icon_url
                }
                box_contents.append(icon)

            baseline_box = {
                "type": "box",
                "layout": "baseline",
                "contents": box_contents,
                "spacing": "sm",
            }

            flex.append(baseline_box)
        return flex

    def _get_share_url(self) -> str:
        query_parameter = parse.urlencode({
            "POIID": self._store.poi_id,
            "POIName": self._store.poi_name,
            "Telno": self._store.tel_no,
            "FaxNo": self._store.fax_no,
            "Address": self._store.address,
            "StoreImageTitle": ' '.join(self._store.service)
        })
        return "?".join([self.line_liff_url, query_parameter])

    def _get_google_map_url(self) -> str:
        google_map_query = parse.quote("7-ELEVEN " + self._store.poi_id + "門市")
        return self.google_map_search_url + google_map_query

    @property
    def flex(self) -> Dict:
        flex = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": self.store_image_url,
                "size": "4xl",
                "aspectRatio": "2:1",
                "aspectMode": "fit"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingTop": "none",
                "contents": [
                    {
                        "type": "text",
                        "text": self._store.poi_name,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "店號",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": self._store.poi_id,
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "電話",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": self._store.tel_no,
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "傳真",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": self._store.fax_no,
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "地址",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": self._store._address,
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "margin": "lg",
                        "contents": self._get_service_flex(7),
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingTop": "xl",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#2E8B57",
                        "height": "md",
                        "action": {
                            "type": "uri",
                            "label": "分享給好友",
                            "uri": self._get_share_url()
                        }
                    },
                    {   
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "uri",
                                    "label": "通話",
                                    "uri": "tel:" + self._store.tel_no
                                }
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "uri",
                                    "label": "地圖",
                                    "uri": self._get_google_map_url()
                                }
                            }
                        ]
                    }
                ]
            }
        }
        return flex


class OtherBubble(Bubble):
    location_image_url = "https://drive.google.com/uc?export=view&id=1kN4KpeevpHXQUtKHa3tbZsUVUWqcSUXI"
    def __init__(self, store: store.Store, key_word: str, n_store: int):
        self._store = store
        self._key_word = key_word
        self._n_store = n_store
        self.body_contents = []

    def __add__(self, other: object) -> object:
        self.body_contents += other.body_contents
        return self

    def create_body_contents(self) -> None:
        self.body_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "md",
                "contents": [
                    {
                        "type": "image",
                        "url": self.location_image_url,
                        "flex": 1,
                        "gravity": "center",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "flex": 5,
                        "contents": [
                            {
                                "type": "text",
                                "text": self._store.poi_name + "門市",
                                "size": "md",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": self._store.address,
                                "size": "sm"
                            }
                        ]
                    }
                ],
                "action": {
                    "type": "message",
                    "label": "action",
                    "text": "小7" + self._store.poi_name
                },
            }
        ]
    
    def _get_hero_text(self) -> str:
        return f"- 點擊搜尋其他 {self._n_store - 1} 間包含「{self._key_word}」的門市 -"

    @property
    def flex(self) -> Dict:
        flex = {
            "type": "bubble", 
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "查看更多小7",
                        "color": "#ffffff",
                        "size": "xl",
                        "weight": "bold",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#2E8B57"
            }, 
            "hero": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": self._get_hero_text(),
                        "color": "#aaaaaa",
                        "size": "sm",
                        "align": "center"
                    }
                ],
                "paddingTop": "lg"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": self.body_contents,
                "spacing": "lg"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": "#2E8B57"
            }
        }
        return flex
        

class LoveFoodBubble(Bubble):
    def __init__(
        self, 
        store: store.Store, 
        list_category_stock_item: List[store.CategoryStockItem],
        update_time: str
    ):
        self._store = store
        self._list_category_stock_item = list_category_stock_item
        self._update_time = update_time

    def _get_detail_item_flex(self, list_item: List[store.StockItem]):
        flex = []
        for stock_item in list_item:
            flex.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": stock_item.name,
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": str(stock_item.remaining_qty),
                        "align": "end"
                    }
                ]
            })
        return flex

    def _get_stock_item_flex(self):
        flex = []
        for category_stock_item in self._list_category_stock_item:
            flex.append({"type": "separator"})
            flex.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": category_stock_item.name,
                        "weight": "bold"
                    }  
                ] + self._get_detail_item_flex(category_stock_item.list_item)
            })
        return flex

    def _get_update_time_text(self):
        datetime_object = datetime.strptime(self._update_time, "%Y-%m-%dT%H:%M:%S")
        datetime_str = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        return "更新時間：" + datetime_str
    
    @property
    def flex(self):
        flex = {
            "type": "bubble", 
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": "https://drive.google.com/uc?export=view&id=1Ut3oitcNiYdlN7EgS1tQ2Yj7CyGIjtJr",
                                "flex": 0,
                                "aspectRatio": "870:346"
                            },
                            {
                                "type": "text",
                                "text": "X " + self._store.poi_name,
                                "flex": 0,
                                "weight": "bold",
                                "size": "xl"
                            }
                        ],
                        "justifyContent": "flex-start",
                        "alignItems": "center",
                        "spacing": "xs"
                    }
                ],
                "paddingStart": "lg",
                "paddingTop": "lg",
                "paddingBottom": "none"
            }, 
            "hero": "",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": self._get_stock_item_flex(),
                "paddingTop": "lg",
                "spacing": "lg"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "separator"
                },
                {
                    "type": "text",
                    "text": self._get_update_time_text(),
                    "size": "xxs",
                    "color": "#aaaaaa"
                }
                ],
                "spacing": "lg"
            }
        }
        return flex