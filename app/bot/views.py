from flask import request, render_template, abort
from decouple import config
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, FlexSendMessage, TextSendMessage
)

from . import bot_blueprint
from ..domain import services


line_bot_api = LineBotApi(config("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(config("LINE_CHANNEL_SECRET"))


@bot_blueprint.route("/share", methods=["GET"])
def share():
    context = {
        "line_liff_url": config("LINE_LIFF_URL"),
        "line_liff_id": config("LINE_LIFF_ID")
    }
    return render_template("bot/share.html", **context)


@bot_blueprint.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(403)
    except LineBotApiError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def store_info(event: MessageEvent):
    factory = TextMessageFactory()
    handler = factory.create_handler(event.message.text)
    handler.handle(event)


class TextMessageFactory:
    def create_handler(self, message: str):
        if message[:2] == "小7":
            return StoreHandler()


class StoreHandler:
    def handle(self, event: MessageEvent):
        key_word = event.message.text[2:]
        try:
            flex = services.to_flex(key_word)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="門市資料", contents=flex)
            )
        except services.InvalidKeyWord:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("無符合條件的門市資料")
            )
        print(event.message.text)
