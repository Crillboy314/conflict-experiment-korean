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
        label='What is your age?',
        min=13, max=125)

    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        label='What is your gender?',
        widget=widgets.RadioSelect)

    education = models.StringField(
        choices=['No schooling','Primary School','Middle School','High School',
        'Some College','Trade/Technical/Vocational Training','Associate Degree',
        'Bachelor\'s Degree','Master\'s Degree','Doctorate'],
        label='What is your highest level of education attained?',
        widget=widgets.RadioSelect)

    language = models.StringField(
        label='What is your native language?',
        widget=widgets.TextInput)

    country = models.StringField(
        label='In which country were you born?',
        widget=widgets.TextInput)

    intent = models.StringField(
        choices=['Selfish','Generous','Hostile','Cooperative','Rational','Irrational'],
        label='What do you think the intent of the other player was in their decisions?',
        widget=widgets.RadioSelect)

    identity = models.StringField(
        choices=['Yes','No','Maybe'],
        label='If you knew the identity of the other player, would you have made a different decision?',
        widget=widgets.RadioSelect)

    risk = models.StringField(
        choices=['0 risk averse','1','2','3','4','5','6','7','8','9','10 fully prepared to take risks'],
        label='How do you rate yourself personally? In general, are you someone who is ready to take risks or do you try to avoid risks? \n Please provide your answers using the scale provided again. 0 means “Not prepared to take risks at all”. 10 means “Prepared to take risks”. You can use the in-between ratings to tailor your response.',        
        widget=widgets.RadioSelect)