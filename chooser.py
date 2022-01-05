def title(t: list):
    return t[0] + " decks cut at " + t[1] + " decks playing $" + t[3] + " with the " + t[2]


class Chooser:
    def __init__(self):
        self.holder = []

    def gather(self):
        decks = input("Choose number of decks (6 or 8): ")
        cut = input("How many decks are cut (1.5, 2 or 2.5): ")
        style = input("(n): no pattern \n (m): martingale system \n (o): oscar's grind \n (c): card counting ")
        per_hand = input("Dollar amount per bet: ")
        see_count = input("See count? (y): yes \n (n): no ")
        self.holder = [decks, cut, style, per_hand, see_count]
        return self.holder


# r = Chooser()
# print(title(r.gather()))
