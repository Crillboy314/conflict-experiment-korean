from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools

author = 'Manolo Noboa'

doc = """
Treatment selector
"""


class Constants(BaseConstants):
    name_in_url = 'selector'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        treatments = itertools.cycle(['default', 't1', 't2'])
        for g in self.get_groups():
            if 'treatment' in self.session.config:
                g.treatment = self.session.config['treatment']
            else:
                g.treatment = next(treatments)
             

class Group(BaseGroup):
    treatment = models.StringField(initial='default')


class Player(BasePlayer):
    pass
