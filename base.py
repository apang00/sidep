# for if game is counted
import random


#######################################################################################################################
#######################################################################################################################
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


def split_cond(player_hand, dealer_hand):
    split_potential = player_hand[0] == player_hand[1]
    nine_split = [2, 3, 4, 5, 6, 8, 9]
    if split_potential and (((dealer_hand[0] in range(2, 8)) and
                             (player_hand[0] == 2 or player_hand[0] == 3 or player_hand[0] == 7)) or
                            (player_hand[0] == 8 or player_hand[0] == 1) or
                            (dealer_hand[0] in range(5, 7) and (player_hand[0] == 4)) or
                            (dealer_hand[0] in range(2, 7) and (player_hand[0] == 6)) or
                            (dealer_hand[0] in nine_split and (player_hand[0] == 9))):
        return True
    # note: never split 5's or 10's for optimal play


#######################################################################################################################
#######################################################################################################################

class Game:

    def __init__(self, decks: int, cut: float, style: str, amount: int,
                 count: bool):

        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0,
                0] * decks  # total number of decks
        self.cut = cut
        self.count = count  # only if this is true is count_holder used
        self.for_count = len(deck * count)  # count needs the cut amount to
        # be taken into consideration
        self.true_count = 0
        random.shuffle(deck)
        self.p_deck = deck[(cut * 52):]

        self.style = style  # depending on if style is necessary
        self.amount = amount

        self.count_holder = []

        self.player = []
        self.dealer = []

    def blackjack_game(self):
        # by basic strategy, no insurance, no even money, double and split by
        # the books

        split_made = False

        for i in range(2):
            self.hit(self.player)
            self.hit(self.dealer)

        # blackjack situations
        self.blackjacks(self.player, self.dealer)

        if self.doubles(self.player, self.dealer):
            self.amount *= 2
        elif split_cond(self.player, self.dealer):
            self.split(self.player)
            split_made = True
        else:
            h_range = [0, 1, 7, 8, 9]
            # keep hitting until player exceeds 16 when dealer shows 7 or higher for optimal play
            while total(self.player) <= 16 and (self.dealer[0] in h_range):
                self.hit(self.player)

        if not split_made:
            if sum(self.player) <= 21:
                if sum(self.player) > self.dealer:
                    return sum(self.player), sum(self.dealer), self.amount, self.counter(self.count_holder)
                elif sum(self.player) == self.dealer:
                    return sum(self.player), sum(self.dealer), 0, self.counter(self.count_holder)
                return sum(self.player), sum(self.dealer), -self.amount, self.counter(self.count_holder)
        else:
            pass

    # ##################################################################################################################

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

    def blackjacks(self, player_hand, dealer_hand):
        if (player_hand == [0, 1] or player_hand == [1, 0]) and (
                dealer_hand == [0, 1] or dealer_hand == [1, 0]):
            return sum(player_hand), sum(dealer_hand), 0, self.counter(
                self.count_holder)

        elif (player_hand == [0, 1] or player_hand == [1, 0]) and (
                dealer_hand != [0, 1] or dealer_hand != [1, 0]):
            return sum(player_hand), sum(
                dealer_hand), self.amount * 1.5, self.counter(self.count_holder)

        elif (player_hand != [0, 1] or player_hand != [1, 0]) and (
                dealer_hand == [0, 1] or dealer_hand == [1, 0]):
            return sum(player_hand), sum(
                dealer_hand), -self.amount, self.counter(self.count_holder)

    def doubles(self, player_hand, dealer_hand):
        # hard doubles
        if total(player_hand) == 11 or \
                (total(player_hand) == 10 and (
                        total(dealer_hand) in range(2, 10))) or \
                (total(player_hand) == 9 and (
                        total(dealer_hand) in range(3, 7))):

            self.hit(player_hand)
            return True

        # soft doubles
        elif (sum(player_hand) == 19 and (1 in player_hand) and
              dealer_hand[0] == 6) or \
                (sum(player_hand) == 18 and (1 in player_hand) and
                 dealer_hand[0] in range(2, 7)) or \
                (sum(player_hand) == 17 and (1 in player_hand) and
                 dealer_hand[0] in range(3, 7)) or \
                (sum(player_hand) == 16 or sum(player_hand) == 15 and
                 (1 in player_hand) and dealer_hand[0] in range(4, 7)) or \
                (sum(player_hand) == 14 or sum(player_hand) == 13 and
                 (1 in player_hand) and dealer_hand[0] in range(5, 7)):

            self.hit(player_hand)
            self.amount *= 2
            return True
        return False

    # note max split is 4 (4 hands)
    def split(self, hand):
        new_hand = {}
        while len(new_hand) <= 4:
            for i in hand:  # hand = [1,1]
                new_hand[self.hit([i])] = self.amount  # {[1, 1]: 10, [1, m]: 5}

#######################################################################################################################
#######################################################################################################################
