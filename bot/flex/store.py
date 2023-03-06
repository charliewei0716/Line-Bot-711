from dataclasses import dataclass, field
from typing import Dict
from urllib import parse


class StoreBubbleBody:
    def __init__(self, store) -> None:
        self._store = store

    def _get_service_flex(self, num):
        flex = []
        for row_start in range(0, len(self._store.service_no), num):
            box_contents = []
            row = self._store.service_no[row_start: row_start+num]

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
    
    def to_flex(self):
        flex = {
            "type": "box",
            "layout": "vertical",
            "paddingTop": "none",
            "contents": [
                {
                    "type": "text",
                    "text": self._store.POI_name,
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
                                    "text": self._store.POI_id,
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
                                    "text": self._store.address,
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
        }
        return flex

class StoreBubbleFooter:
    def __init__(self, store, line_liff_url) -> None:
        self._store = store
        self._line_liff_url = line_liff_url

    def _get_share_url(self):
        query_parameter = parse.urlencode({
            "POIID": self._store.POI_id,
            "POIName": self._store.POI_name,
            "Telno": self._store.tel_no,
            "FaxNo": self._store.fax_no,
            "Address": self._store.address,
            "StoreImageTitle": ' '.join(self._store.service_no)
        })
        return "?".join([self._line_liff_url, query_parameter])

    def to_flex(self):
        flex = {
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
                                "uri": self._store.tel_no_url
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "uri",
                                "label": "地圖",
                                "uri": self._store.google_map_url
                            }
                        }
                    ]
                }
            ]
        }
        return flex


class StoreBubble:
    def __init__(self, body_flex, footer_flex) -> None:
        self._hero = self._get_hero_flex()
        self._body = body_flex.to_flex()
        self._footer = footer_flex.to_flex()

    def _get_hero_flex(self) -> Dict:
        flex = {
            "type": "image",
            "url": "https://drive.google.com/uc?export=view&id=1bh8pHsrrbFhtPb57CAO8-l0CzSjlo_5m",
            "size": "4xl",
            "aspectRatio": "2:1",
            "aspectMode": "fit"
        }
        return flex

    def to_flex(self):
        flex = {
            "type": "bubble",
            "hero": self._hero,
            "body": self._body,
            "footer": self._footer
        }
        return flex


