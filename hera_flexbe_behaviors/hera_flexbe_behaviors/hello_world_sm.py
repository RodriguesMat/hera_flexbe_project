# hello_world_sm.py
from flexbe_core import Behavior, Autonomy, OperatableStateMachine
from flexbe_core.proxy import ProxyLogger
from hera_flexbe_project_flexbe_states.states.hello_state import HelloState

class HelloWorldSM(Behavior):
    """
    Behavior mínimo com um único estado que loga e finaliza.
    Outcomes:
        - finished
        - failed
    """

    def __init__(self):
        super().__init__()
        self.name = 'HelloWorld'
        self._logger = ProxyLogger.create()

    def create(self):
        sm = OperatableStateMachine(outcomes=['finished', 'failed'])

        with sm:
            OperatableStateMachine.add('SayHello',
                HelloState(text="Olá do FlexBE v4!"),
                transitions={'done': 'finished'},
                autonomy={'done': Autonomy.Off})

        return sm
