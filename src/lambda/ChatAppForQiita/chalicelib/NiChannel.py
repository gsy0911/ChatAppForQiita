from chalicelib.CommandExecutor import CommandExecutor
import os
from datetime import datetime
import hashlib
import requests
import json
import re


class NiChannel(CommandExecutor):
    def __init__(self):
        super().__init__("/2ch")
        # メッセージの送信先
        self.url = 'https://slack.com/api/chat.postMessage'

    def get_username(self, text: str, user_id: str, now_str: str) -> (str, str, str):
        hashed_id = hashlib.md5((now_str + user_id).encode()).hexdigest()[:9]
        ptn = r'(\[([^#]+)(\#([a-zA-Z0-9]+))?\])?(.*)'
        ret = re.match(ptn, text, flags=(re.MULTILINE | re.DOTALL))

        username = ret.group(2)
        password = ret.group(4)
        main_text = ret.group(5)

        self.logger.info(f"{username}, {password}")

        default_name = "名無し"
        if username is not None and password is not None:
            hashed_name = hashlib.md5(password.encode()).hexdigest()[:8]
            default_name = f"{username[:8]}◆{hashed_name}"
            hashed_id = "????????"
        elif username is not None:
            default_name = username[:16].replace("◆", "◇")

        return default_name, hashed_id, main_text

    def execute(self, params: dict) -> dict:
        now = datetime.now()
        now_str = now.strftime("%Y/%m/%d %H:%M:%S")
        user_id = params['user_id'][0]
        text = " ".join(params['text'])
        self.logger.info(f"user_id:={user_id}, text:={text}")

        access_token = os.environ['OAUTH_ACCESS_TOKEN']
        channel_id = os.environ['CHANNEL_ID']

        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json; charset=utf-8'
        }

        username, hashed_id, main_text = self.get_username(text, user_id, now_str)

        data = {
            "channel": channel_id,
            "text": main_text,
            "username": f"[No]{username}：{now_str} ID：{hashed_id}"
        }
        json_data = json.dumps(data).encode("utf-8")
        ret = requests.post(self.url, data=json_data, headers=headers)
        status_code = ret.status_code
        body = ret.content.decode('utf-8')
        self.logger.info(f"status_code:= {status_code}, body:={body}")
        return {
            "text": f"posted successfully"
        }
