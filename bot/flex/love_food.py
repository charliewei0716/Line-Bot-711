from datetime import datetime
import math


class LoveFoodBubbleBody:
    n_item_in_bubble = 5

    def __init__(self, love_food_scraper, ith_bubble) -> None:
        self._stock_item = love_food_scraper.stock_item
        self._ith_bubble = ith_bubble

    @classmethod
    def calculate_n_bubble(cls, n_item):
        return math.ceil(n_item/5)

    def _in_bubble(self, ith_item):
        return self.n_item_in_bubble*self._ith_bubble <= ith_item < self.n_item_in_bubble*(self._ith_bubble+1)

    def _get_detail_item_flex(self, item_list):
        flex = []
        for detail_item in item_list:
            flex.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": detail_item["ItemName"],
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": str(detail_item["RemainingQty"]),
                        "align": "end"
                    }
                ]
            })
        return flex

    def _get_stock_item_flex(self):
        flex = []
        for index, stock_item in enumerate(self._stock_item):
            if self._in_bubble(index):
                flex.append({"type": "separator"})
                flex.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": stock_item["Name"],
                            "weight": "bold"
                        }  
                    ] + self._get_detail_item_flex(stock_item["ItemList"])
                })
        return flex

    def to_flex(self):
        flex = {
            "type": "box",
            "layout": "vertical",
            "contents": self._get_stock_item_flex(),
            "paddingTop": "lg",
            "spacing": "lg"
        }
        return flex


class LoveFoodBubbleFooter:
    def __init__(self, love_food_scraper):
        self._update_time = love_food_scraper.update_time

    def _get_update_time_text(self):
        datetime_object = datetime.strptime(self._update_time, "%Y-%m-%dT%H:%M:%S")
        datetime_str = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        return "更新時間：" + datetime_str

    def to_flex(self):
        flex =  {
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
        return flex


class LoveFoodBubble:
    def __init__(self, store, love_food_bubble_body, love_food_bubble_footer) -> None:
        self._store_name = store.POI_name
        self._header = self._get_header_flex()
        self._body = love_food_bubble_body.to_flex()
        self._footer = love_food_bubble_footer.to_flex()

    def _get_header_flex(self):
        flex = {
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
                            "text": "X " + self._store_name,
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
        }
        return flex

    def to_flex(self):
        flex = {
            "type": "bubble", 
            "header": self._header, 
            "hero": "",
            "body": self._body,
            "footer": self._footer
        }
        return flex