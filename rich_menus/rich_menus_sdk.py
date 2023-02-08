import requests
import json
from linebot import LineBotApi

class RichMenus():

    RICHMENUS_ENDPOINT = "https://api.line.me/v2/bot/richmenu"
    USER_ALL_RICHMENUS_ENDPOINT = "https://api.line.me/v2/bot/user/all/richmenu/"

    def __init__(
        self, channel_access_token, richmenus_endpoint=RICHMENUS_ENDPOINT,
        user_all_richmenus_endpoint=USER_ALL_RICHMENUS_ENDPOINT
    ):
        self.richmenus_endpoint = richmenus_endpoint
        self.user_all_richmenus_endpoint = user_all_richmenus_endpoint
        self.headers = {
            "Authorization": "Bearer " + channel_access_token,
            "Content-Type":"application/json"
        }
        self.line_bot_api = LineBotApi(channel_access_token)

    def create(self, rich_menus_body, content_type, content):

        response = requests.post(
            self.richmenus_endpoint, headers=self.headers, data=json.dumps(rich_menus_body)#.encode('utf-8')
        ).json()

        richMenuId = response["richMenuId"]

        self.line_bot_api.set_rich_menu_image(richMenuId, content_type, content)

        response = requests.post(
            self.user_all_richmenus_endpoint + richMenuId, headers=self.headers
        ).json()

        return response

    def delete_all(self):
        rich_menu_list = self.line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            self.line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)


if __name__ == '__main__':

    import os
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent

    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(BASE_DIR, ".dev.env"))
    except:
        pass

    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

    rich_menus = RichMenus(LINE_CHANNEL_ACCESS_TOKEN)

    rich_menus.delete_all()

    rich_menus_body = {
        "size": {"width": 2500, "height": 843},
        "selected": "true",
        "name": "start",
        "chatBarText": "點我開始",
        "areas":[
            {
            "bounds": {"x": 0, "y": 0, "width": 2500, "height": 843},
            "action": {"type": "message", "text": "小7亞萬"}
            }
        ]
    }

    with open(os.path.join(BASE_DIR, "rich_menus", "line_rich_menus.jpg"), 'rb') as f:
        rich_menus.create(rich_menus_body, "image/jpeg", f)