from typing import Dict

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c)

doc = """
This is a decision making activity, where the player picks one of 5 gambles.
"""


class Constants(BaseConstants):
    name_in_url = 'gamble'
    players_per_group = 2
    num_rounds = 1
    # Payoffs depending on the situation

    payoff_matrix: Dict[str, Dict[int, c]] = {
        'A':
            {
                1: c(16),
                2: c(24),
                3: c(32),
                4: c(40),
                5: c(48)
            },
        'B':
            {
                1: c(16),
                2: c(12),
                3: c(8),
                4: c(4),
                5: c(0)
            }
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gamble_number = models.IntegerField(
        choices=[1, 2, 3, 4, 5],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    gain = models.CurrencyField(initial=c(0))
    event = models.StringField()

    def set_gain(self, r):
        self.event = r
        self.gain = Constants.payoff_matrix[self.event][self.gamble_number]
        self.payoff += self.gain
