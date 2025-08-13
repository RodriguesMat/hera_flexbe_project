from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from hera_msgs.srv import Beep as BeepSrv

class BeepState(EventState):
    """Toca um beep usando o serviço `beep`.

    Outcomes:
        - done: serviço executado
        - failed: erro ou result == False
    """

    def __init__(self, frequency=700, duration=400, service_name='beep'):
        super().__init__(outcomes=['done', 'failed'])
        self._srv = service_name
        self._proxy = ProxyServiceCaller({self._srv: BeepSrv})
        self._req = BeepSrv.Request()
        self._req.frequency = int(frequency)
        self._req.duration = int(duration)
        self._res = None

    def on_enter(self, userdata):
        self._res = None
        try:
            self._res = self._proxy.call(self._srv, self._req)
        except Exception as e:
            Logger.logwarn(f"[BeepState] Falha ao chamar serviço: {e}")

    def execute(self, userdata):
        if self._res is None:
            return 'failed'
        return 'done' if getattr(self._res, 'result', False) else 'failed'
