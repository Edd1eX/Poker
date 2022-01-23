# coding=utf-8
import settings
import classes
from tkinter import *


s = classes.Statistics(2)

score = None
trumpNumbers = None
suits = None
types = None
d = None
decks = None


def count():
    global score, trumpNumbers
    score.set(s.getScore())
    trumpNumbers.set(s.getTrumpNumbers())


def play(suit, type, d):
    s.play(suit, type)
    d.setText(suit, type, s.getCards(suit, type))
    count()


def recorder(root):
    row = 1
    cards = Frame(root, relief='solid', borderwidth=1)

    for type in settings.types:
        Label(cards, text=type, font=('宋体', 9)).grid(row=row, column=0, sticky=E)
        row += 1
    column = 1
    for suit in settings.suits:
        if suit != settings.joker:
            Label(cards, text=suit, font=('宋体', 9)).grid(row=0, column=column)
            column += 1

    row = 5
    for type in settings.jokers:
        Label(cards, text=type, font=('宋体', 9)).grid(row=row, column=column, columnspan=2)
        row += 3

    global d
    d = classes.drawer()
    column = 1
    for suit in settings.suits:
        row = 1
        if suit != settings.joker:
            for type in settings.types:
                Button(cards, textvariable=d.getText(suit, type), height=2, width=4,
                       command=lambda suit=suit, type=type: play(suit, type, d)).grid(row=row, column=column)
                d.setText(suit, type, s.getCards(suit, type))
                row += 1
        else:
            row = 6
            for type in settings.jokers:
                Button(cards, textvariable=d.getText(suit, type), height=2, width=4,
                       command=lambda suit=suit, type=type: play(suit, type, d)).\
                    grid(row=row, column=column, columnspan=2)
                d.setText(suit, type, s.getCards(suit, type))
                row += 3
        column += 1

    return cards


def set_trump_suit(suit):
    s.setTrumpSuit(suit)
    count()


def trump_suit(root):
    trump = Frame(root, relief='solid', borderwidth=1)
    Label(trump, text='主牌花色').grid(row=0, column=0, columnspan=2)
    row = 1
    global suits
    suits = StringVar()
    for suit in settings.suits:
        Radiobutton(trump, text=suit, variable=suits, value=suit, command=lambda suit=suit: set_trump_suit(suit)).\
            grid(row=row, column=0, sticky=W)
        row += 1
    return trump


def set_level(level):
    s.setLevel(level)
    count()


def level(root):
    l = Frame(root, relief='solid', borderwidth=1)
    Label(l, text='级别').grid(row=0, column=0, columnspan=3)

    global types
    types = StringVar()

    row = 1
    column = 0
    for type in settings.types:
        Radiobutton(l, text=type, variable=types, value=type, command=lambda level=type: set_level(level)).\
            grid(row=row, column=column, sticky=W)
        column += 1
        if column >= 3:
            column -= 3
            row += 1

    return l


def set_decks(decks):
    s.setDecks(decks)


def deckSetting(root):
    deck = Frame(root, relief='solid', borderwidth=1)
    Label(deck, text='牌副数', font=('宋体', 9)).grid(row=0, column=0, columnspan=4, pady=3)
    column = 0
    global decks
    decks = IntVar()
    for num in [1, 2, 3, 4]:
        Radiobutton(deck, text=num, variable=decks, value=num, height=1, width=3, bd=1,
                    command=lambda decks=num: set_decks(decks), indicatoron=0).\
            grid(row=1, column=column, sticky=W, padx=2, pady=1)
        column += 1
    decks.set(2)
    set_decks(decks.get())
    return deck


def counter(root):
    c = Frame(root, relief='solid', borderwidth=1)

    global score, trumpNumbers
    score = StringVar()
    trumpNumbers = StringVar()

    Label(c, text='计数器').grid(row=0, column=0, columnspan=2)
    Label(c, text='剩余分数').grid(row=1, column=0)
    Label(c, text='剩余主牌数').grid(row=2, column=0)
    Label(c, textvariable=score).grid(row=1, column=1)
    Label(c, textvariable=trumpNumbers).grid(row=2, column=1)
    return c


def selectModule(root):
    module = Frame(root)
    # 主牌花色选定组件
    trump_suit(module).grid(row=0, column=0, sticky=N, padx=5)
    # 级别选定组件
    level(module).grid(row=0, column=1, sticky=N, padx=5)
    # 牌副数选定组件
    deckSetting(module).grid(row=1, column=0, columnspan=2, padx=5, pady=10)
    # 计数器组件
    counter(module).grid(row=2, columnspan=2, pady=90)
    return module


def reset():
    suits.set(settings.suits[0])
    types.set(settings.types[0])
    s.setTrumpSuit(suits.get())
    s.setLevel(types.get())
    d.reset(s)
    count()


def _reset(root):
    rst = Frame(root, relief='solid', borderwidth=1)
    Button(rst, text='重置', command=reset).pack()
    return rst


def _exit(root):
    ext = Frame(root, relief='solid', borderwidth=1)
    Button(ext, text='退出', command=root.quit).pack()
    return ext


def buttonModule(root):
    module = Frame(root)
    # 重置模块
    _reset(module).grid(row=0, column=0, padx=20)
    # 退出模块
    _exit(module).grid(row=0, column=1, padx=20)
    return module


def init():
    root = Tk()
    root.title("升级记牌器 " + settings.vesion)
    root.geometry('420x650')
    root.geometry('-150-200')
    root.wm_attributes('-topmost', 1)

    module = Frame(root)

    selectModule(module).grid(row=0, column=0)
    buttonModule(module).grid(row=1, column=0, pady=100)

    module.grid(row=0, column=0, sticky=N, pady=2)

    # 记牌器组件
    recorder(root).grid(row=0, column=2, padx=5, pady=2, sticky=N)

    reset()
    count()

    root.mainloop()


def main():
    init()


if __name__ == '__main__':
    main()
