from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


doc = """
This is a decision-making activity. Two participants send messages and are asked separately
whether they want option A or option B with different symbols. Their choices directly determine the
payoffs to each of the participants.
"""


class Constants(BaseConstants):
    name_in_url = 'control2'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'control2/Instructions.html'
    message_template = 'control2/Message.html'

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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
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
    ask_used = models.BooleanField(initial=False)
    ask_answer = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        widget=widgets.RadioSelect,
        label="Your answer:"
    )

    def set_payoff(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        payoff_matrix = {
            'L':
                {
                    'L': Constants.both_L_payoff,
                    'R': Constants.YouL_OpponentR_payoff
                },
            'R':
                {
                    'L': Constants.YouR_OpponentL_payoff,
                    'R': Constants.both_R_payoff
                }
        }
        p1.payoff = payoff_matrix[p1.decision][p2.decision] + Constants.endowment - p1.paid_msg * Constants.message_cost
        p2.payoff = payoff_matrix[p2.decision][p1.decision] + Constants.endowment - p2.paid_msg * Constants.message_cost

    def check_Ask(self):
        N = self.send_message == 'ask' or self.send_answer == 'ask'
        Y = self.ask_used and self.ask_answer
        return N and Y


class Player(BasePlayer):
    decision = models.StringField(
        choices=['L', 'R'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )
    paid_msg = models.IntegerField(initial=0)

    def use_paid_message(self):
        self.paid_msg += 1
        self.group.ask_used = True
        return self.payoff

    def other_player(self):
        return self.get_others_in_group()[0]

    question_1 = models.IntegerField(
    label = "Suppose that you are First Person, and that you select your right symbol, what would be your payout if Second Person also chooses their right symbol?",
    min=10,max=70)

    question_2 = models.IntegerField(
    label = "Suppose that you are Second Person, you select your right symbol, what would be your payout if the First Person chooses their left symbol?",
    min=10,max=70)
