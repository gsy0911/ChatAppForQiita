from chalicelib.CommandExecutor import CommandExecutor
from chalicelib.NiChannel import NiChannel
from chalicelib.Hoge import Hoge
from chalicelib.Fuga import Fuga


class CommandExecutorRequestHandler(CommandExecutor):
    """
    最初にメッセージを受け取り、処理を開始するクラス
    このRequestHandlerではメッセージの受け取りを担うのみで
    実際の処理を行うのはset_next()内に含まれるインスタンスが処理を行う
    """
    def __init__(self):
        """
        self.set_next({instance}).set_next({instance})
        のように数珠繋ぎに関数をつなげる
        """
        super().__init__("RequestHandler")
        # commandに拠って出力する内容を切り替える
        self.set_next(Hoge()).set_next(Fuga()).set_next(NiChannel())
