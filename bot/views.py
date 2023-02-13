from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    FlexSendMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

import json
import requests
from bs4 import BeautifulSoup
from urllib import parse
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
line_liff_url = settings.LINE_LIFF_URL

def share(request):
    context = {
        "line_liff_url": line_liff_url
    }
    return render(request, "share.html", context=context)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.type == "text":
                    if event.message.text[:2] == "小7":

                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

                        form_data = {
                            "commandid": "SearchStore",
                            'StoreName': event.message.text[2:]
                        }

                        data = parse.urlencode(form_data)

                        response = requests.post("https://emap.pcsc.com.tw/EMapSDK.aspx", headers=headers, data=data)

                        soup = BeautifulSoup(response.text, "xml")

                        # print(soup.prettify())

                        n_store = len(soup.find_all("POIID"))

                        if n_store>0:
                            bubble_contents = []
                            for i_store in range(n_store):
                                if i_store==5:
                                    break
                                POIID = soup.find_all("POIID")[i_store].get_text().strip()
                                POIName = soup.find_all("POIName")[i_store].get_text().strip()
                                Telno = soup.find_all("Telno")[i_store].get_text().strip()
                                FaxNo = soup.find_all("FaxNo")[i_store].get_text().strip()
                                Address = soup.find_all("Address")[i_store].get_text().strip()
                                list_StoreImageTitle = soup.find_all("StoreImageTitle")[i_store].get_text().split(",")
                                list_StoreImageTitle = [store_service[:2] for store_service in list_StoreImageTitle]

                                uri_Telno = "tel:" + Telno
                                google_map_query = parse.quote("7-ELEVEN "+POIName+"門市")
                                uri_Address = "https://www.google.com/maps/search/?api=1&query=" + google_map_query

                                print(list_StoreImageTitle)

                                query_parameter = parse.urlencode({
                                    "POIID": POIID,
                                    "POIName": POIName,
                                    "Telno": Telno,
                                    "FaxNo": FaxNo,
                                    "Address": Address,
                                    "StoreImageTitle": ' '.join(list_StoreImageTitle)
                                })

                                list_StoreImageTitle = [
                                    list_StoreImageTitle[i: i+7] for i in range(0, len(list_StoreImageTitle), 7)
                                ]

                                line_icon_box_contents = []
                                for i_line in list_StoreImageTitle:
                                    icon_box_contents = []
                                    for store_service in i_line:
                                        icon_url = f"https://emap.pcsc.com.tw/menuImg/service_{store_service}.jpg"

                                        icon = {
                                            "type": "icon",
                                            "size": "xxl",
                                            "url": icon_url
                                        }

                                        icon_box_contents.append(icon)

                                    baseline_box = {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": icon_box_contents,
                                        "spacing": "sm",
                                    }

                                    line_icon_box_contents.append(baseline_box)

                                bubble_hero = {
                                    "type": "image",
                                    "url": "https://drive.google.com/uc?export=view&id=1bh8pHsrrbFhtPb57CAO8-l0CzSjlo_5m",
                                    "size": "4xl",
                                    "aspectRatio": "2:1",
                                    "aspectMode": "fit"
                                }

                                bubble_body = {
                                    "type": "box",
                                    "layout": "vertical",
                                    "paddingTop": "none",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": POIName,
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
                                                            "text": POIID,
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
                                                            "text": Telno,
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
                                                            "text": FaxNo,
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
                                                            "text": Address,
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
                                            "contents": line_icon_box_contents,
                                        }
                                    ]
                                }

                                bubble_footer = {
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
                                                "uri": "?".join([line_liff_url, query_parameter])
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
                                                        "uri": uri_Telno
                                                    }
                                                },
                                                {
                                                    "type": "button",
                                                    "style": "secondary",
                                                    "action": {
                                                        "type": "uri",
                                                        "label": "地圖",
                                                        "uri": uri_Address
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }

                                bubble = {
                                    "type": "bubble",
                                    "hero": bubble_hero,
                                    "body": bubble_body,
                                    "footer":bubble_footer
                                }

                                bubble_contents.append(bubble)

                            contents = {
                                "type": "carousel",
                                "contents": bubble_contents
                            }

                            line_bot_api.reply_message(
                                event.reply_token,
                                FlexSendMessage(alt_text="門市資料", contents=contents)
                            )

                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage("無符合條件的門市資料")
                            )

                print(event.message.text)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()