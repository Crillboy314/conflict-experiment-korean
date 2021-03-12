from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'language',
                   'country',
                   'education']

class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['risk',
                   'intent',
                   'identity']

page_sequence = [
    Demographics,
    CognitiveReflectionTest
]
