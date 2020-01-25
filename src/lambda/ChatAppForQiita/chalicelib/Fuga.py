from chalicelib.CommandExecutor import CommandExecutor


class Fuga(CommandExecutor):
    def __init__(self):
        super().__init__("/fuga")

    def execute(self, params: dict) -> dict:
        # x-www-form-urlencodedではjsonのパラメータがリストでデコードされるため
        text = params['text'][0]
        self.logger.info(f"text:={text}")

        # slash commandから直接レスポンスを返す
        return {
            "response_type": "in_channel",
            "text": f"[fuga]{text}"
        }
