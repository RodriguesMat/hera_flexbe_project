from flexbe_core import Behavior, OperatableStateMachine
from hera_flexbe_behaviors.states.beep_state import BeepState
from hera_flexbe_behaviors.states.hear_state import HearState
from hera_flexbe_behaviors.states.match_state import MatchState
from hera_flexbe_behaviors.states.chat_state import ChatState
from hera_flexbe_behaviors.states.speak_state import SpeakState

class ListenAndRespondSM(Behavior):
    """Fluxo: Beep -> Hear -> (opcional Match) -> Chat -> Speak

    Userdata inicial:
        specs: list[str] (para o match)
        use_match: bool (habilita passo de match)
    """

    def __init__(self):
        super().__init__()
        self.name = 'Listen And Respond'

    def create(self):
        sm = OperatableStateMachine(outcomes=['finished', 'failed'])
        sm.userdata.heard_text = ''
        sm.userdata.answer = ''
        sm.userdata.specs = []
        sm.userdata.use_match = False

        with sm:
            # 1) Beep
            OperatableStateMachine.add('Beep',
                BeepState(frequency=700, duration=400, service_name='beep'),
                transitions={'done': 'Hear', 'failed': 'failed'})

            # 2) Hear
            OperatableStateMachine.add('Hear',
                HearState(service_name='hear'),
                transitions={'done': 'DecideMatch', 'empty': 'failed', 'failed': 'failed'},
                remapping={'heard_text': 'heard_text'})

            # 2.1) Decisão
            OperatableStateMachine.add('DecideMatch',
                _ChoiceState(['do', 'skip'], lambda ud: 'do' if ud.use_match else 'skip'),
                transitions={'do': 'Match', 'skip': 'Chat'})

            # 3) Match (opcional)
            OperatableStateMachine.add('Match',
                MatchState(function='object', service_name='match'),
                transitions={'found': 'Chat', 'not_found': 'Chat', 'failed': 'failed'},
                remapping={'text': 'heard_text', 'specs': 'specs', 'matched_text': 'heard_text'})

            # 4) Chat
            OperatableStateMachine.add('Chat',
                ChatState(service_name='chat'),
                transitions={'done': 'Speak', 'failed': 'failed'},
                remapping={'question': 'heard_text', 'answer': 'answer'})

            # 5) Speak
            OperatableStateMachine.add('Speak',
                SpeakState(service_name='speak'),
                transitions={'done': 'finished', 'failed': 'failed'},
                remapping={'text': 'answer'})

        return sm

from flexbe_core import EventState
class _ChoiceState(EventState):
    def __init__(self, outcomes, chooser):
        super().__init__(outcomes=outcomes, input_keys=['use_match'])
        self._chooser = chooser
    def execute(self, userdata):
        return self._chooser(userdata)
