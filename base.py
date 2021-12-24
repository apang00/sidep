import os
import random

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

    def __init__(self, decks: int, cut: float, style: str, amount: int, count: bool):
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0] * decks
        self.cut = cut
        self.style = style
        self.amount = amount
        self.count = count  # only if this is true is count_holder used
        self.count_holder = []
        self.win = 0
        self.player = []
        self.dealer = []

    def deal(self, player):
        random.shuffle(self.deck)
        for i in range(2):
            card = self.deck.pop()
            player.append(card)
            self.count_holder.append(card)

    def hit(self, hand: list):
        card = self.deck.pop()
        self.count_holder.append(card)
        hand.append(card)

    def clear(self):
        if os.name == 'nt':
            os.system('CLS')
        if os.name == 'posix':
            os.system('clear')

    def blackjack(self):
        # by basic strategy, no insurance, no even money, double and split by the books

        self.deal(self.player)
        self.deal(self.dealer)

        # blackjack situations
        if (self.player == [0, 1] or self.player == [1, 0]) and (self.dealer == [0, 1] or self.dealer == [1, 0]):
            self.win = 0
        elif (self.player == [0, 1] or self.player == [1, 0]) and (self.dealer != [0, 1] or self.dealer != [1, 0]):
            self.win = self.amount * 1.5
        elif (self.player != [0, 1] or self.player != [1, 0]) and (self.dealer == [0, 1] or self.dealer == [1, 0]):
            self.win = -self.amount

        # non-blackjack hands
        # double situations
        h_range = [0, 1, 7, 8, 9]
        if total(self.player) == 11 or \
                (total(self.player) == 10 and (total(self.dealer) in range(2, 10))) or \
                (total(self.player) == 9 and (total(self.dealer) in range(3, 7))):

            self.hit(self.player)
            self.amount *= 2

        # split situations
        elif self.player[0] == self.player[1]:




        else:
            # keep hitting until player either reaches past 16 if dealer shows 7 or higher
            while total(self.player) <= 16 and (self.dealer[0] in h_range):
                self.hit(self.player)

    def check_payout(self):
        if total(self.player) > 21:
            self.win = -self.amount
            return True
        elif total(self.dealer) > 21:
            self.win = self.amount
            return True
