from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from hera_msgs.srv import Hear as HearSrv

class HearState(EventState):
    """Chama o serviço `hear` para ouvir/transcrever.

    Output Keys:
        - heard_text (str)

    Outcomes:
        - done: texto capturado
        - failed: erro
        - empty: texto vazio
    """

    def __init__(self, service_name='hear'):
        super().__init__(outcomes=['done', 'failed', 'empty'], output_keys=['heard_text'])
        self._srv = service_name
        self._proxy = ProxyServiceCaller({self._srv: HearSrv})
        self._res = None

    def on_enter(self, userdata):
        self._res = None
        try:
            req = HearSrv.Request()  # sem campos
            self._res = self._proxy.call(self._srv, req)
        except Exception as e:
            Logger.logwarn(f"[HearState] Falha: {e}")

    def execute(self, userdata):
        if self._res is None:
            return 'failed'
        text = getattr(self._res, 'text', '') or ''
        userdata.heard_text = text
        if len(text.strip()) == 0:
            return 'empty'
        return 'done'
