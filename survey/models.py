from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    age = models.IntegerField(
        label='나이(만 ____세):',
        min=13, max=125)

    gender = models.StringField(
        choices=['남성 ', '여성', '기타'],
        label='성별:',
        widget=widgets.RadioSelect)

    education = models.StringField(
        choices=['무학','초등학교 졸업','중학교 졸업','고등학교 졸업',
        '대학교 재학 또는 중퇴','무역/기술/직업 교육','2년제 대학 학위',
        '4년제 대학 학위','석사 학위','박사 학위'],
        label='당신의 최종 학력은 무엇입니까?',
        widget=widgets.RadioSelect)

    language = models.StringField(
        label='모국어',
        widget=widgets.TextInput)

    country = models.StringField(
        label='태어난 나라',
        widget=widgets.TextInput)

    intent = models.StringField(
        choices=['이기적','관대한','적대적','협력적','이성적','비이성적'],
        label='귀하는 상대방 참가자가 결정을 할 때 어떤 의도를 지니고 있었다고 생각하십니까?',
        widget=widgets.RadioSelect)

    identity = models.StringField(
        choices=['예','아니오','아마도'],
        label='만약 귀하가 같이 게임을 한 상대방 참가자가 누구인지 알았다면, 다른 선택을 내렸을 것이라고 생각하십니까?',
        widget=widgets.RadioSelect)

    risk = models.StringField(
        choices=['0 – 위험을 회피하는','1','2','3','4','5','6','7','8','9','10 – 위험을 감수할 준비가 충분히 되어 있음'],
        label='귀하는 자신을 개인적으로 어떻게 평가하십니까? 일반적으로 기꺼이 위험을 감수하는 사람입니까, 아니면 위험을 피하려고 합니까? 제공된 척도를 사용하여 답변을 해 주십시오. 0은 "전혀 위험을 감수할 준비가 되어 있지 않음"을 의미합니다. 10은 "위험을 감수할 준비가 되어 있음"을 의미합니다. 귀하는 0-10 사이의 숫자를 사용하여 답변할 수 있습니다.',
        widget=widgets.RadioSelect)