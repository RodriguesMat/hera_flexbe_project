from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from hera_msgs.srv import Speak as SpeakSrv

class SpeakState(EventState):
    """Faz a Hera falar um texto via serviço `speak`.

    Input Keys:
        - text (str)

    Outcomes:
        - done: falou com sucesso
        - failed: erro
    """

    def __init__(self, service_name='speak'):
        super().__init__(outcomes=['done', 'failed'], input_keys=['text'])
        self._srv = service_name
        self._proxy = ProxyServiceCaller({self._srv: SpeakSrv})
        self._res = None

    def on_enter(self, userdata):
        self._res = None
        try:
            req = SpeakSrv.Request()
            req.text = str(userdata.text) if hasattr(userdata, 'text') else ''
            self._res = self._proxy.call(self._srv, req)
        except Exception as e:
            Logger.logwarn(f"[SpeakState] Falha: {e}")

    def execute(self, userdata):
        if self._res is None:
            return 'failed'
        return 'done' if getattr(self._res, 'success', False) else 'failed'
