from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(WaitPage):
    template_name = 'selector/MyPage.html'

    def app_after_this_page(self, upcoming_apps):
        t = self.group.treatment
        if t == 'default':
            return "controltrial"
        elif t == 't1':
            return "control1trial"
        else:
            return "control2trial"


page_sequence = [
    MyPage
]
