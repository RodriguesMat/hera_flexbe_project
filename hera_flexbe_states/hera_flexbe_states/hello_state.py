# hello_state.py
from flexbe_core import EventState, Logger

class HelloState(EventState):
    """
    State mínimo que loga um texto e termina.
    Outcomes:
        - done: sempre retorna após logar.
    """
    def __init__(self, text: str = "Hello, FlexBE!"):
        super().__init__(outcomes=['done'])
        self._text = text

    def execute(self, userdata):
        Logger.loginfo(f"[HelloState] {self._text}")
        return 'done'
