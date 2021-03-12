from ._builtin import Page
from random import randint


class GambleInstructions(Page):
    form_model = 'player'
    form_fields = ['gamble_number']

    def vars_for_template(self):
        return{
            'erpoint': self.session.config['real_world_currency_per_point'] * 100
        }

    def before_next_page(self):
        event = randint(0, 100)
        if event <= 50:
            self.player.set_gain('A')
        else:
            self.player.set_gain('B')


class GambleResults(Page):
    form_model = 'player'


page_sequence = [
    GambleInstructions,
    GambleResults
]
