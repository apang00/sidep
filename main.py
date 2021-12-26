from chooser import Chooser
from base import Game


class Play:

    def __init__(self, decks, cut, style, amount, count):
        self.decks = decks
        self.cut = cut
        self.amount = amount
        self.style = style
        self.count = count
        self.results = []

    def run_game(self):
        i = Chooser()
        decks = i.gather()[0]
        cut = i.gather()[1]
        style = i.gather()[3]
        amount = i.gather()[4]
        count = i.gather()[5]
        if style == "n":
            n = Game(decks, cut, "n", amount, count)
        elif style == "m":
            m = Game(decks, cut, "m", amount, count)
        elif style == "o":
            o = Game(decks, cut, "o", amount, count)
        elif style == "c":
            c = Game(decks, cut, "c", amount, count)

    def csv_extract(self):
        return self.results

    # every betting pattern will return a list at the end
    # ([hand #, player cards, dealer cards, W/L])
