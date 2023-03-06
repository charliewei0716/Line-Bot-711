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

from .scrape.store import WebScraper, StoreScraper
from .scrape.love_food import LoveFoodScraper
from .flex.store import StoreBubble, StoreBubbleBody, StoreBubbleFooter
from .flex.love_food import LoveFoodBubble, LoveFoodBubbleBody, LoveFoodBubbleFooter
from .flex.other import OtherBubble, OtherBubbleBody, OtherBubbleHero
from .flex.carousel import Carousel

lovefood_mid_v = settings.LOVEFOOD_MID_V
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
line_liff_url = settings.LINE_LIFF_URL
line_liff_id = settings.LINE_LIFF_ID

def share(request):
    context = {
        "line_liff_url": line_liff_url,
        "line_liff_id": line_liff_id
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
                        web_scraper = WebScraper(event.message.text[2:])
                        store_scraper = StoreScraper(web_scraper.soup)

                        # print(soup.prettify())

                        if not store_scraper.n_store == 0:

                            main_store = store_scraper.main_store()

                            carousel = Carousel()

                            # The main store bubble
                            store_bubble_body = StoreBubbleBody(main_store)
                            store_bubble_footer = StoreBubbleFooter(main_store, line_liff_url)
                            store_bubble = StoreBubble(store_bubble_body, store_bubble_footer)
                            carousel.add_bubble(store_bubble)
                            
                            # The love food bubble
                            love_food_scraper = LoveFoodScraper(main_store)
                            love_food_bubble_footer = LoveFoodBubbleFooter(love_food_scraper)
                            for ith_bubble in range(LoveFoodBubbleBody.calculate_n_bubble(love_food_scraper.n_stock_item)):
                                love_food_bubble_body = LoveFoodBubbleBody(love_food_scraper, ith_bubble)
                                love_food_bubble = LoveFoodBubble(main_store, love_food_bubble_body, love_food_bubble_footer)
                                carousel.add_bubble(love_food_bubble)

                            if store_scraper.n_store > 1:
                                # The other store bubble
                                other_bubble_hero = OtherBubbleHero(web_scraper, store_scraper)
                                other_bubble_body = OtherBubbleBody(store_scraper)
                                other_bubble = OtherBubble(other_bubble_hero, other_bubble_body)
                                carousel.add_bubble(other_bubble)

                            contents=carousel.to_flex()
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