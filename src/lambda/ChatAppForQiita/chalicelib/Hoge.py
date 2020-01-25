from chalicelib.CommandExecutor import CommandExecutor


class Hoge(CommandExecutor):
    def __init__(self):
        super().__init__("/hoge")

    def execute(self, params: dict) -> dict:
        # x-www-form-urlencodedではjsonのパラメータがリストでデコードされるため
        text = params['text'][0]
        self.logger.info(f"text:={text}")

        # slash commandから直接レスポンスを返す
        return {
            "response_type": "in_channel",
            "text": f"[hoge]{text}"
        }
