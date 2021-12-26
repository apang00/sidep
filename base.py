# for if game is counted

def total(hand):
    tot = 0
    for card in hand:
        if card == 0:
            tot += 10
        elif card == 1:
            if tot >= 11:
                tot += 1
            else:
                tot += 11
        else:
            tot += card
    return tot


class Game:

    def __init__(self, decks: int, cut: float, style: str, amount: int,
                 count: bool):

        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0,
                0] * decks  # total number of decks
        self.count = count  # only if this is true is count_holder used
        self.p_deck = deck * (decks - count)  # playable deck, count included
        self.cut = cut
        self.for_count = len(deck * count)  # count needs the cut amount to
        # be taken into consideration
        self.true_count = 0

        self.style = style  # depending on if style is necessary
        self.amount = amount

        self.count_holder = []
        self.win = 0

        self.player = []
        self.dealer = []

    def hit(self, hand: list):
        if self.p_deck:
            card = self.p_deck.pop()
            self.count_holder.append(card)
            hand.append(card)
        else:
            self.reset()

    def reset(self):
        pass  # restart the game, if reset happens mid-game, money goes back
        # and nothing happens, game is not counted

        # running count only

    def counter(self, cards):
        plus = [i for i in range(2, 7)]
        minus = [1, 0]
        counter = 0
        for i in cards:
            if i in plus:
                counter += 1
            elif i in minus:
                counter -= 1
            else:
                counter += 0

        self.true_count += counter / (len(self.p_deck) + self.for_count)
        return self.true_count

    def blackjack(self):
        # by basic strategy, no insurance, no even money, double and split by
        # the books

        split_potential = self.player[0] == self.player[1]

        for i in range(2):
            self.hit(self.player)
            self.hit(self.dealer)

        # blackjack situations
        if (self.player == [0, 1] or self.player == [1, 0]) and (
                self.dealer == [0, 1] or self.dealer == [1, 0]):
            return sum(self.player), sum(self.dealer), 0, self.counter(
                self.count_holder)
        elif (self.player == [0, 1] or self.player == [1, 0]) and (
                self.dealer != [0, 1] or self.dealer != [1, 0]):
            return sum(self.player), sum(
                self.dealer), self.amount * 1.5, self.counter(self.count_holder)
        elif (self.player != [0, 1] or self.player != [1, 0]) and (
                self.dealer == [0, 1] or self.dealer == [1, 0]):
            return sum(self.player), sum(
                self.dealer), -self.amount, self.counter(self.count_holder)

        # non-blackjack hands
        # double situations (hard doubles)
        h_range = [0, 1, 7, 8, 9]
        nine_split = [2, 3, 4, 5, 6, 8, 9]
        if total(self.player) == 11 or \
                (total(self.player) == 10 and (
                        total(self.dealer) in range(2, 10))) or \
                (total(self.player) == 9 and (
                        total(self.dealer) in range(3, 7))):

            self.hit(self.player)
            self.amount *= 2

        # soft doubles
        elif (sum(self.player) == 19 and (1 in self.player) and
              self.dealer[0] == 6) or \
                (sum(self.player) == 18 and (1 in self.player) and
                 self.dealer[0] in range(2, 7)) or \
                (sum(self.player) == 17 and (1 in self.player) and
                 self.dealer[0] in range(3, 7)) or \
                (sum(self.player) == 16 or sum(self.player) == 15 and
                 (1 in self.player) and self.dealer[0] in range(4, 7)) or \
                (sum(self.player) == 14 or sum(self.player) == 13 and
                 (1 in self.player) and self.dealer[0] in range(5, 7)):

            self.hit(self.player)
            self.amount *= 2

        # split situations 2's and 3's and 7's
        elif split_potential and (self.dealer[0] in range(2, 8)) and \
                (self.player[0] == 2 or self.player[0] == 3 or self.player[
                    0] == 7):
            self.split(self.player)

        # splits mandatory for 8 and A
        elif split_potential and self.player[0] == 8 or self.player[0] == 1:
            self.split(self.player)

        # splits for 4,6 and 9
        elif split_potential and self.dealer[0] in range(5, 7) and \
                (self.player[0] == 4):
            self.split(self.player)
        elif split_potential and self.dealer[0] in range(5, 7) and \
                (self.player[0] == 6):
            self.split(self.player)
        elif split_potential and self.dealer[0] in nine_split and \
                (self.player[0] == 9):
            self.split(self.player)
        # note: never split 5's or 10's for optimal play

        else:
            # keep hitting until player either reaches past 16 if dealer
            # shows 7 or higher
            while total(self.player) <= 16 and (self.dealer[0] in h_range):
                self.hit(self.player)

        if not split_potential and (sum(self.player)) <= 21:
            if sum(self.player) > self.dealer:
                return sum(self.player), sum(self.dealer), self.win, \
                       self.counter(self.count_holder)
            elif sum(self.player) == self.dealer:
                return sum(self.player), sum(self.dealer), 0, \
                       self.counter(self.count_holder)
            return sum(self.player), sum(self.dealer), -self.win, self.counter(
                self.count_holder)

    # gotta think of sum for this...
    def split(self, hand):
        hand[0] = [hand[0], self.hit(hand[0])]
