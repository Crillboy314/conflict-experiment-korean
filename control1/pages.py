from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


# class Introduction(Page):
#     def vars_for_template(self):
#         return {
#             'sufee' : self.session.config['participation_fee'],
#             'erpoint' : self.session.config['real_world_currency_per_point']*100
#         }
#
#
# class Tree(Page):
#     pass


class SendMessageP1(Page):
    form_model = 'group'
    form_fields = ['send_message']
    template_name = 'control1/SendMessage.html'

    def is_displayed(self):
        return self.player.id_in_group == 1


class Wait(WaitPage):
    pass


class SendMessageP2(Page):
    form_model = 'group'
    form_fields = ['send_answer']
    template_name = 'control1/SendMessage.html'

    def is_displayed(self):
        return self.player.id_in_group == 2


class DecisionP1(Page):
    template_name = 'control1/Decision.html'
    form_model = 'player'
    form_fields = ['decision']

    def is_displayed(self):
        return self.player.id_in_group == 1


class DecisionP2(Page):
    template_name = 'control1/Decision.html'
    form_model = 'player'
    form_fields = ['decision']

    def is_displayed(self):
        return self.player.id_in_group == 2


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()
        return {
            'my_decision': me.decision,
            'opponent_decision': opponent.decision,
            'same_choice': me.decision == opponent.decision,
        }

    def app_after_this_page(self, upcoming_apps):
        return 'gamble'


# class Quiz(Page):
#     form_model = 'player'
#     form_fields = ['question_1', 'question_2']
#
#     def error_message(self, values):
#         if values['question_1'] != 40 and values['question_2'] != 20:
#             return 'Both questions are incorrect'
#         elif values['question_1'] == 40 and values['question_2'] != 20:
#             return 'Question 2 is incorrect'
#         elif values['question_1'] != 40 and values['question_2'] == 20:
#             return 'Question 1 is incorrect'


page_sequence = [
    # Introduction,
    # Tree,
    # Quiz,
    SendMessageP1,
    Wait,
    SendMessageP2,
    Wait,
    DecisionP1,
    Wait,
    DecisionP2,
    ResultsWaitPage,
    Results
]
