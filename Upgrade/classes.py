import settings
from tkinter import *


class Statistics:
    cards = {}
    decks = 2
    trump_suit = ""
    level = ""
    trump_numbers = 0
    score = 0

    def __init__(self, decks):
        self.decks = decks
        self.reset()

    def getCards(self, suit, type):
        return self.cards[suit][type]

    def getScore(self):
        return self.score

    def getTrumpNumbers(self):
        return self.trump_numbers

    def play(self, suit, type):
        if suit in self.cards and type in self.cards[suit]:
            if self.cards[suit][type] > 0:
                self.cards[suit][type] = self.cards[suit][type] - 1
                if suit == self.trump_suit or type == self.level or suit == settings.joker:
                    self.trump_numbers -= 1
                if type in settings.scores:
                    self.score -= settings.scores[type]

    def setTrumpSuit(self, suit):
        self.trump_suit = suit
        self.calTrumpNumbers()

    def setLevel(self, level):
        self.level = level
        self.calTrumpNumbers()

    def setDecks(self, decks):
        self.decks = decks
        self.calTrumpNumbers()

    ##########################################
    def calTrumpNumbers(self):
        # 未设定主牌花色
        if self.trump_suit not in settings.suits:
            self.trump_numbers = 0
        # 未设定级别
        elif self.level not in settings.types:
            sum = 0
            # 主花色数量
            if self.trump_suit != settings.joker:
                for type in settings.types:
                    sum += self.cards[self.trump_suit][type]
            # 王数量
            for type in settings.jokers:
                sum += self.cards[settings.joker][type]
            self.trump_numbers = sum
        # 全都已经设定
        else:
            sum = 0
            # 正常亮主
            if self.trump_suit != settings.joker:
                # 主花色数量
                for type in settings.types:
                    sum += self.cards[self.trump_suit][type]

                for suit in settings.suits:
                    # 王数量
                    if suit == settings.joker:
                        for type in settings.jokers:
                            sum += self.cards[suit][type]
                    # 主数量
                    elif suit != self.trump_suit:
                        sum += self.cards[suit][self.level]
            # 无主
            else:
                for suit in settings.suits:
                    # 王数量
                    if suit == settings.joker:
                        for type in settings.jokers:
                            sum += self.cards[suit][type]
                    # 主数量
                    else:
                        sum += self.cards[suit][self.level]
            self.trump_numbers = sum

    def calScore(self):
        sum = 0
        for suit in settings.suits:
            if suit != settings.joker:
                for score in settings.scores:
                    sum += self.cards[suit][score] * settings.scores[score]
        self.score = sum

    def reset(self):
        for suit in settings.suits:
            if suit == settings.joker:
                for type in settings.jokers:
                    if suit not in self.cards:
                        self.cards[suit] = {}
                    self.cards[suit][type] = self.decks
            else:
                for type in settings.types:
                    if suit not in self.cards:
                        self.cards[suit] = {}
                    self.cards[suit][type] = self.decks
        self.trump_suit = ""
        self.level = ""
        self.trump_numbers = 0
        self.score = 0
        self.calScore()


class drawer:
    cards = {}

    def __init__(self):
        for suit in settings.suits:
            if suit == settings.joker:
                for type in settings.jokers:
                    if suit not in self.cards:
                        self.cards[suit] = {}
                    btn_text = StringVar()
                    self.cards[suit][type] = btn_text
            else:
                for type in settings.types:
                    if suit not in self.cards:
                        self.cards[suit] = {}
                    btn_text = StringVar()
                    self.cards[suit][type] = btn_text

    def reset(self, s):
        for suit in settings.suits:
            if suit != settings.joker:
                for type in settings.types:
                    self.setText(suit, type, s.getCards(suit, type))
            else:
                for type in settings.jokers:
                    self.setText(suit, type, s.getCards(suit, type))

    def getText(self, suit, type):
        return self.cards[suit][type]

    def setText(self, suit, type, content):
        # print(suit, type, content)
        self.cards[suit][type].set(content)

    def check(self):
        print(self.cards)
