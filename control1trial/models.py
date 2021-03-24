from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)
import random

doc = """
This is a decision-making activity that includes messages with a common dictionary. 
Two participants are asked separately whether they want option A or option B. Their choices directly determine the
payoffs to each of the participants.
"""


class Constants(BaseConstants):
    name_in_url = 'control1trial'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'control1/Instructions.html'

    #Payoffs depending on the situation

    YouA_OpponentB_payoff = c(70)
    YouB_OpponentA_payoff = c(20)


    both_B_payoff = c(40)
    both_A_payoff = c(10)

    payoff_matrix = {
        'A':
            {
                'A': both_A_payoff,
                'B': YouA_OpponentB_payoff
            },
        'B':
            {
                'A': YouB_OpponentA_payoff,
                'B': both_B_payoff
            }
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bot_decision = models.StringField(
        choices=['A', 'B'],
        doc="""This player's bot decision""",
        widget=widgets.RadioSelect
    )

    send_message = models.StringField(
        label="What message do you want to send to Second Person?",
        choices=[
            ['A', 'I choose A'],
            ['B', 'I choose B']
        ],
        widget=widgets.RadioSelect
    )

    send_answer = models.StringField(
        label="What message do you want to send to First Person?",
        choices=[
            ['A', 'I choose A'],
            ['B', 'I choose B']
        ],
        widget=widgets.RadioSelect
    )

    decision = models.StringField(
        choices=['A', 'B'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    question_1 = models.IntegerField(
        label="귀하가 첫 번째 사람이고 B를 선택했다고 가정할 때, 두 번째 사람도 B를 선택하면 귀하는 몇 점을 획득하게 됩니까?",
        min=10, max=70)

    question_2 = models.IntegerField(
        label="귀하가 두 번째 사람이고 B를 선택했다고 가정할 때, 첫 번째 사람이 A를 선택하면 귀하는 몇 점을 획득하게 됩니까?",
        min=10, max=70)

    trial_payoff = models.CurrencyField(initial=0)

    def rand_send_message(self):
        self.send_message = random.choice(['A', 'B'])

    def rand_send_answer(self):
        self.send_answer = random.choice(['A', 'B'])

    def other_player(self):
        return self.get_others_in_group()[0]

    def bot_result(self):
        self.bot_decision = random.choice(['A', 'B'])

    def set_payoff(self):
        self.trial_payoff = Constants.payoff_matrix[self.decision][self.bot_decision]
