from chooser import Chooser


class Patterns:

    def __init__(self, decks: int, cut: float, style: str, amount: int, count: bool):
        self.decks = decks
        self.cut = cut
        self.amount = amount
        self.style = style
        self.count = count

    def run_game(self):
        i = Chooser()
        decks = i.gather()[0]


    # every betting pattern will return a list at the end
    # ([hand #, player cards, dealer cards, W/L])
