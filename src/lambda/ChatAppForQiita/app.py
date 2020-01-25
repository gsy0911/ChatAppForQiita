from chalice import Chalice
import os
import logging
from chalicelib.CommandExecutorRequestHandler import CommandExecutorRequestHandler
import urllib.parse
app = Chalice(app_name='ChatAppForQiita')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def recieve_command():
    request = app.current_request
    if request.raw_body is None:
        # 予期しない呼び出し。400 Bad Requestを返す
        return {'statusCode': 400}
    payload = urllib.parse.parse_qs(request.raw_body.decode('utf-8'))
    logger.info(f"payload:= {payload}")

    token = os.environ['SLACK_TOKEN']
    request_token = payload['token'][0]

    if request_token != token:
        # 送信元の確認
        return {'ok': False, "error": "token not matched"}

    request_handler = CommandExecutorRequestHandler()
    return request_handler.handle_execute(payload)
