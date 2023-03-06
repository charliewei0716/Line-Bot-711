
class OtherBubbleHero:
    def __init__(self, web_scraper, store_scraper) -> None:
        self._store_name = web_scraper.store_name
        self._n_store = store_scraper.n_store
    
    def to_flex(self):
        hero_text = f"- 點擊搜尋其他 {self._n_store -1 } 間包含「{self._store_name}」的門市 -"
        flex = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": hero_text,
                    "color": "#aaaaaa",
                    "size": "sm",
                    "align": "center"
                }
            ],
            "paddingTop": "lg"
        }
        return flex


class OtherBubbleBody:
    def __init__(self, store_scraper) -> None:
        self._other_store = store_scraper.other_store()
    
    def _get_other_store_flex(self):
        flex = []
        for store in self._other_store:
            flex.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://drive.google.com/uc?export=view&id=1kN4KpeevpHXQUtKHa3tbZsUVUWqcSUXI",
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
                                    "text": store.POI_name + "門市",
                                    "size": "md",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": store.address,
                                    "size": "sm"
                                }
                            ]
                        }
                    ],
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": "小7" + store.POI_name
                    },
                }
            )
        return flex
    
    def to_flex(self):
        flex = {
            "type": "box",
            "layout": "vertical",
            "contents": self._get_other_store_flex(),
            "spacing": "lg"
        }
        return flex


class OtherBubble:
    def __init__(self, hero, body) -> None:
        self._header = self._get_header_flex()
        self._hero = hero.to_flex()
        self._body = body.to_flex()
        self._footer = self._get_footer_flex()

    def _get_header_flex(self):
        flex = {
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
        }
        return flex

    def _get_footer_flex(self):
        flex = {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "backgroundColor": "#2E8B57"
        }
        return flex

    def to_flex(self):
        flex = {
            "type": "bubble", 
            "header": self._header, 
            "hero": self._hero,
            "body": self._body,
            "footer": self._footer
        }
        return flex