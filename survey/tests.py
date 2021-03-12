from otree.api import Currency as c, currency_range

from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):

        yield (pages.Demographics, {
            'age': 24,
            'gender': 'Male'})

        yield (pages.CognitiveReflectionTest, {
            'education': 'Primary School',
            'intent': 'Generous',
            'identity': 'Maybe'
        })