from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def vars_for_template(self):
        return {
            'sufee' : self.session.config['participation_fee'],
            'erpoint' : self.session.config['real_world_currency_per_point']*100
        }


class Tree1(Page):
    pass


class Tree2(Page):
    pass


class RLC_P1(Page):
    template_name = 'control2trial/Message.html'
    form_model = 'player'
    form_fields = ['send_message']

    def is_displayed(self):
        a = self.player.send_message == 'ask' or self.player.send_message is None
        if self.player.pNum == 1:
            b = True
        else:
            if a:
                self.player.rand_send_messageRLC()
            b = False
        return a and b

    def send_message_choices(self):
        choices = [
                ['LC', '나는' + Constants.P1_codified_L + '를 선택합니다.'],
                ['RC', '나는' + Constants.P1_codified_R + '를 선택합니다.']
        ]
        if not self.player.ask_used:
            choices.append(
                ['ask', '5점의 비용을 지불하고 다른 참가자에게 그림의 어느 쪽을 선택할 계획인지 물어보겠습니다.']
            )
        return choices

    def before_next_page(self):
        if self.player.send_message == 'ask':
            self.player.use_paid_message()


class Wait(WaitPage):
    pass


class RLC_P2(Page):
    template_name = 'control2trial/Message.html'
    form_model = 'player'
    form_fields = ['send_answer']

    def is_displayed(self):
        a = self.player.send_answer is None or self.player.send_answer == 'ask'
        if self.player.pNum == 2:
            b = True
        else:
            if a:
                self.player.rand_send_answerRLC()
            b = False
        return a and b

    def send_answer_choices(self):
        choices = [
            ['LC', '나는' + Constants.P2_codified_L + '를 선택합니다.'],
            ['RC', '나는' + Constants.P2_codified_R + '를 선택합니다.']
        ]
        if not self.player.ask_used:
            choices.append(
                ['ask', '5점의 비용을 지불하고 다른 참가자에게 그림의 어느 쪽을 선택할 계획인지 물어보겠습니다.']
            )
        return choices

    def before_next_page(self):
        if self.player.send_answer == 'ask':
            self.player.use_paid_message()


class YesNo_P1(Page):
    template_name = 'control2trial/YesNo.html'
    form_model = 'player'
    form_fields = ['ask_answer']

    def is_displayed(self):
        b = self.player.ask_used and self.player.send_answer == 'ask'
        if self.player.pNum == 1:
            a = True
        else:
            if b:
                self.player.rand_ask_answer()
            a = False
        return a and b

    def before_next_page(self):
        if not self.player.ask_answer and self.player.ask_answer is not None:
            self.player.use_paid_message()


class YesNo_P2(Page):
    template_name = 'control2trial/YesNo.html'
    form_model = 'player'
    form_fields = ['ask_answer']

    def is_displayed(self):
        b = self.player.ask_used and self.player.send_message == 'ask'
        if self.player.pNum == 2:
            a = True
        else:
            if b:
                self.player.rand_ask_answer()
            a = False
        return a and b

    def before_next_page(self):
        if not self.player.ask_answer and self.player.ask_answer is not None:
            self.player.use_paid_message()


class RL_P1(Page):
    template_name = 'control2trial/RL.html'
    form_model = 'player'
    form_fields = ['send_message']

    def is_displayed(self):
        b = self.player.check_Ask()
        if self.player.pNum == 1:
            a = True
        else:
            if b:
                self.player.rand_send_messageRL()
            a = False

        return a and b

    def send_message_choices(self):
        choices = [['L', 'I choose'], ['R', 'I choose']]
        return choices


class RL_P2(Page):
    template_name = 'control2trial/RL.html'
    form_model = 'player'
    form_fields = ['send_answer']

    def is_displayed(self):
        b = self.player.check_Ask()
        if self.player.pNum == 2:
            a = True
        else:
            if b:
                self.player.rand_send_answerRL()
            a = False
        return a and b

    def send_answer_choices(self):
        choices = [['L', 'I choose'], ['R', 'I choose']]
        return choices


class DecisionP1(Page):
    form_model = 'player'
    form_fields = ['decision']
    template_name = 'control2trial/Decision.html'

    def decision_choices(self):
        if self.player.pNum == 1:
            choices = [
                ['L',Constants.P1_codified_L],
                ['R',Constants.P1_codified_R]
            ]
        else:
            choices = [
                ['L', Constants.P2_codified_L],
                ['R', Constants.P2_codified_R]
            ]
        return choices

    def is_displayed(self):
        if self.player.id_in_group == 1:
            return True
        else:
            self.player.bot_result()
            return False


class DecisionP2(Page):
    form_model = 'player'
    form_fields = ['decision']
    template_name = 'control2trial/Decision.html'

    def decision_choices(self):
        if self.player.pNum == 1:
            choices = [
                ['L',Constants.P1_codified_L],
                ['R',Constants.P1_codified_R]
            ]
        else:
            choices = [
                ['L', Constants.P2_codified_L],
                ['R', Constants.P2_codified_R]
            ]
        return choices

    def is_displayed(self):
        if self.player.id_in_group == 2:
            return True
        else:
            self.player.bot_result()
            return False


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


# class Results(Page):
#     def vars_for_template(self):
#         me = self.player
#         return {
#             'my_decision': me.decision,
#             'opponent_decision': me.bot_decision,
#             'same_choice': me.decision == me.bot_decision
#         }
#
#     def app_after_this_page(self, upcoming_apps):
#         return 'control2'


class Quiz(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2']

    def error_message(self, values):
        if values['question_1'] != 40 and values['question_2'] != 20:
            return 'Both questions are incorrect'
        elif values['question_1'] == 40 and values['question_2'] != 20:
            return 'Question 2 is incorrect'
        elif values['question_1'] != 40 and values['question_2'] == 20:
            return 'Question 1 is incorrect'


page_sequence = [
    Introduction,
    Tree1,
    Tree2,
    Quiz,
    RLC_P1,
    YesNo_P2,
    RL_P2,
    RL_P1,
    RLC_P2,
    YesNo_P1,
    RL_P1,
    RL_P2,
    RLC_P1,
    RLC_P2,
    DecisionP1,
    # Wait,
    DecisionP2,
    ResultsWaitPage
    # Results
]
