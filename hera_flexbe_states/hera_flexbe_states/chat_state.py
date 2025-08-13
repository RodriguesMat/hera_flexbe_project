from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from hera_msgs.srv import Chat as ChatSrv

class ChatState(EventState):
    """Envia `question` ao serviço `chat` e retorna `answer`.

    Input Keys:
        - question (str)

    Output Keys:
        - answer (str)

    Outcomes:
        - done: sucesso
        - failed: erro
    """

    def __init__(self, service_name='chat'):
        super().__init__(outcomes=['done', 'failed'], input_keys=['question'], output_keys=['answer'])
        self._srv = service_name
        self._proxy = ProxyServiceCaller({self._srv: ChatSrv})
        self._res = None

    def on_enter(self, userdata):
        self._res = None
        try:
            req = ChatSrv.Request()
            req.question = str(getattr(userdata, 'question', ''))
            self._res = self._proxy.call(self._srv, req)
        except Exception as e:
            Logger.logwarn(f"[ChatState] Falha: {e}")

    def execute(self, userdata):
        if self._res is None:
            return 'failed'
        userdata.answer = getattr(self._res, 'answer', '')
        return 'done' if len(userdata.answer) > 0 else 'failed'
