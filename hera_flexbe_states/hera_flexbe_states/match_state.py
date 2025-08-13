from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from hera_msgs.srv import Match as MatchSrv

class MatchState(EventState):
    """Verifica se algum item em `specs` aparece no `text` via serviço `match`.

    Input Keys:
        - text (str)
        - specs (list[str])

    Output Keys:
        - matched_text (str)
        - matched (bool)

    Outcomes:
        - found: result True
        - not_found: result False
        - failed: erro
    """

    def __init__(self, function='object', service_name='match'):
        super().__init__(
            outcomes=['found', 'not_found', 'failed'],
            input_keys=['text', 'specs'],
            output_keys=['matched_text', 'matched']
        )
        self._srv = service_name
        self._proxy = ProxyServiceCaller({self._srv: MatchSrv})
        self._function_default = function
        self._res = None

    def on_enter(self, userdata):
        self._res = None
        try:
            req = MatchSrv.Request()
            req.text = str(getattr(userdata, 'text', ''))
            req.specs = list(getattr(userdata, 'specs', []))
            req.function = self._function_default
            self._res = self._proxy.call(self._srv, req)
        except Exception as e:
            Logger.logwarn(f"[MatchState] Falha: {e}")

    def execute(self, userdata):
        if self._res is None:
            return 'failed'
        userdata.matched_text = getattr(self._res, 'text', '')
        userdata.matched = bool(getattr(self._res, 'result', False))
        return 'found' if userdata.matched else 'not_found'
