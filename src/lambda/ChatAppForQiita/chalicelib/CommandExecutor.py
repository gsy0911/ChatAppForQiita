import logging


class ChainOfResponsibilityException(Exception):
    pass


class CommandExecutor:
    """
    Chain of Responsibility（処理の移譲）というデザインパターンに基づいている。

    また、CommandExecutorRequestHandlerクラスのインスタンスを起点として
    メッセージの読み取りを始め、処理の移譲をおこなう。
    """
    def __init__(self, command):
        self.command = command
        self.next_executor = None
        # ログの出力フォーマットはAWS標準に準拠
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def set_next(self, next_decoder):
        self.next_executor = next_decoder
        return next_decoder

    def check_responsibility(self, params) -> bool:
        """
        このクラスが対処すべきコマンドかどうか判定
        """
        if 'command' not in params:
            return False
        if len(params['command']) == 0:
            return False
        return self.command == params['command'][0]

    def handle_execute(self, params) -> dict:
        """
        入力された`params`の実行元（`command`）によって
        実行する処理を変更する関数

        1. 呼ばれたクラスのコマンド(self.command)がcommandと等しい場合、処理を行う
          * デコード処理が正しく行われた場合は、処理結果を返し、【終了】
          * 正しく行われなかった場合は、異常という処理結果を返し、【終了】

        2. 呼ばれたクラスの名前がcommandと異なる場合、次のクラスに処理を任せる : self.next_execute(params)
          * 次のクラスがある場合、処理が【続く】
          * 次のクラスがない場合、異常という処理結果を返し、【終了】

        """
        # 対象のCommandかどうか確認
        if self.check_responsibility(params):
            result_dict = self.execute(params)
            if len(result_dict) > 0:
                # メッセージの処理に成功した場合は処理結果を返す
                return result_dict
            else:
                # メッセージの処理に失敗した場合は例外を投げる
                raise ChainOfResponsibilityException

        elif self.next_executor is not None:
            # 対象のCommandでは無い場合、次のexecutorに任せる
            # [Chain of Responsibility]の部分
            return self.next_executor.handle_execute(params)
        else:
            return {"error": "Could not execute your command. Check your {/command} name"}

    def execute(self, params) -> dict:
        """
        各クラスで担うべき処理を実装する
        """
        pass

    def __str__(self):
        return f'[{self.command}]'
