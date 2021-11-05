from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)

import random


doc = """
This is a decision-making activity. Two participants send messages and are asked separately
whether they want option A or option B with different symbols. Their choices directly determine the
payoffs to each of the participants.
"""


class Constants(BaseConstants):
    name_in_url = 'control2trial'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'control2/Instructions.html'

    endowment = c(5)
    message_cost = c(5)

    # Payoffs depending on the situation

    YouL_OpponentR_payoff = c(70)
    YouR_OpponentL_payoff = c(20)

    both_R_payoff = c(40)
    both_L_payoff = c(10)

    # Characters for codified messages
    P1_codified_R = '@'
    P1_codified_L = '#'
    P2_codified_R = '*'
    P2_codified_L = '&'

    Bot_codified_R = '%'
    Bot_codified_L = '^'

    payoff_matrix = {
        'L':
            {
                'L': both_L_payoff,
                'R': YouL_OpponentR_payoff
            },
        'R':
            {
                'L': YouR_OpponentL_payoff,
                'R': both_R_payoff
            }
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            #p.pNum = random.choice([1, 2])
            p.pNum = p.id_in_group


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pNum = models.IntegerField()

    def set_payoff(self):
        self.trial_payoff = Constants.payoff_matrix[self.decision][self.bot_decision] + Constants.endowment - self.paid_msg * Constants.message_cost

    def check_Ask(self):
        try:
            N = self.send_message == 'ask'
        except TypeError:
            try:
                N = self.send_answer == 'ask'
            except TypeError:
                N = False
        Y = self.ask_used and self.ask_answer
        return N and Y

    ask_used = models.BooleanField(initial=False)

    def get_bot_decision(self):
        try:
            return self.bot_decision
        except TypeError:
            return False

    bot_decision = models.StringField(
        choices=[['L', Constants.Bot_codified_L], ['R', Constants.Bot_codified_R]],
        doc="""This player's bot decision""",
        widget=widgets.RadioSelect
    )

    def get_ask_answer(self):
        try:
            return self.ask_answer
        except TypeError:
            return False

    ask_answer = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        widget=widgets.RadioSelect,
        label="Your answer:"
    )



    def get_send_answer(self):
        try:
            return self.send_answer
        except TypeError:
            return False

    send_answer = models.StringField(
        # label = "What option do you want the participant A to think you will chose?",
        choices=[
            ['L', 'the Left side'],
            ['R', 'the Right side'],
            ['LC', Constants.P2_codified_L],
            ['RC', Constants.P2_codified_R],
            ['ask', 'A']
        ],
        widget=widgets.RadioSelect
    )

    def send_answer_choices(self):
        choices = [
            ['LC', '나는 ' + Constants.P2_codified_L + '를 선택합니다.'],
            ['RC', '나는 ' + Constants.P2_codified_R + '를 선택합니다.']
        ]
        if not self.ask_used:
            choices.append(
                ['ask', '5점의 비용을 지불하고 다른 참가자에게 그림의 어느 쪽을 선택할 계획인지 물어보겠습니다.']
            )
        return choices

    def get_send_message(self):
        try:
            return self.send_message
        except TypeError:
            return False

    send_message = models.StringField(
        # label = "What option do you want the participant B to think you will chose?",
        choices=[
            ['L', 'the Left side'],
            ['R', 'the Right side'],
            ['LC', Constants.P1_codified_L],
            ['RC', Constants.P1_codified_R],
            ['ask', 'A']
        ],
        widget=widgets.RadioSelect
    )

    def send_message_choices(self):
        choices = [
                ['LC', '나는 ' + Constants.P1_codified_L + '를 선택합니다.'],
                ['RC', '나는 ' + Constants.P1_codified_R + '를 선택합니다.']
        ]
        if not self.ask_used:
            choices.append(
                ['ask', '5점의 비용을 지불하고 다른 참가자에게 그림의 어느 쪽을 선택할 계획인지 물어보겠습니다.']
            )
        return choices

    def get_bot_answer(self):
        try:
            a = self.bot_answer
        except TypeError:
            return random.choice(['LC', 'RC', 'ask', 'L', 'R'])
        return a

    bot_answer = models.StringField(
        choices=[
            ['L', 'the Left side'],
            ['R', 'the Right side'],
            ['LC', Constants.Bot_codified_L],
            ['RC', Constants.Bot_codified_R],
            ['ask', 'A']
        ]
    )

    def rand_send_messageRLC(self):
        if not self.ask_used:
            self.send_message = random.choice(['LC', 'RC', 'ask'])
        else:
            self.send_message = random.choice(['LC', 'RC'])
        self.bot_answer = self.send_message

    def rand_send_messageRL(self):
        self.send_message = random.choice(['L', 'R'])

    def rand_send_answerRLC(self):
        if not self.ask_used:
            self.send_answer = random.choice(['LC', 'RC', 'ask'])
        else:
            self.send_answer = random.choice(['LC', 'RC'])
        self.bot_answer = self.send_answer

    def bot_result(self):
        self.bot_decision = random.choice(['L', 'R'])

    def rand_send_answerRL(self):
        self.send_answer = random.choice(['L', 'R'])

    def rand_ask_answer(self):
        self.ask_answer = random.choice([True, False])

    decision = models.StringField(
        choices=['L', 'R'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    def decision_choices(self):
        if self.pNum == 1:
            choices = [
                ['L', Constants.P1_codified_L],
                ['R', Constants.P1_codified_R]
            ]
        else:
            choices = [
                ['L', Constants.P2_codified_L],
                ['R', Constants.P2_codified_R]
            ]
        return choices

    paid_msg = models.IntegerField(initial=0)
    trial_payoff = models.CurrencyField(initial=0)

    def use_paid_message(self):
        self.paid_msg += 1
        self.ask_used = True
        return self.payoff

    question_1 = models.IntegerField(
        label = "귀하가 첫 번째 사람이고 오른쪽 기호를 선택했다고 가정할 때, 두 번째 사람도 오른쪽 기호를 선택하면 귀하는 몇 점을 획득하게 됩니까?",
        min=10,max=70)

    question_2 = models.IntegerField(
        label = "귀하가 두 번째 사람이고 오른쪽 기호를 선택했다고 가정할 때, 첫 번째 사람이 왼쪽 기호를 선택하면 귀하는 몇 점을 획득하게 됩니까?",
        min=10,max=70)
