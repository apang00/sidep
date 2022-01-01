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
    if player_hand[0] == player_hand[1]:
        split_potential = True
    else:
        split_potential = False

    nine_split = [2, 3, 4, 5, 6, 8, 9]
    if split_potential and (((dealer_hand[0] in range(2, 8)) and
                             (player_hand[0] == 2 or player_hand[0] == 3 or player_hand[0] == 7)) or
                            (player_hand[0] == 8 or player_hand[0] == 1) or
                            (dealer_hand[0] in range(5, 7) and (player_hand[0] == 4)) or
                            (dealer_hand[0] in range(2, 7) and (player_hand[0] == 6)) or
                            (dealer_hand[0] in nine_split and (player_hand[0] == 9))):
        return True
    return False
    # note: never split 5's or 10's for optimal play


#######################################################################################################################
#######################################################################################################################

def blackjack_cond(player, dealer):
    if (total(player) == 21 and len(player) == 2) or (total(dealer) == 21 and len(dealer) == 2):
        return True
    return False


class Game:

    def __init__(self, dex: int, cut: float, style: str, amount: int,
                 count: bool):

        self.decks = dex
        self.cut = cut
        self.count = count  # only if this is true is count_holder used
        self.for_count = self.cut * 52  # count needs the cut amount to be taken into consideration
        self.true_count = 0

        self.style = style  # depending on if style is necessary
        self.amount = amount

        self.split_hand = {}
        self.count_holder = []

    def setup(self):
        # deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0] * 4 * self.decks  # normal deck
        # deck = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0] * 4 * self.decks  # blackjack tests passed
        deck = [8, 3, 8, 8, 8, 3, 3, 8, 3, 8, 3, 8] * 4 * self.decks
        random.shuffle(deck)
        return deck[(52 * self.cut):]

    def blackjack_game(self, p_deck):
        player = []
        dealer = []

        for i in range(2):
            self.hit(player, p_deck)
            self.hit(dealer, p_deck)

        # blackjack situations
        if blackjack_cond(player, dealer):
            return self.blackjacks(player, dealer, p_deck)

        if self.doubles(player, dealer, p_deck):
            self.amount *= 2
            return self.reg_play_dealer(player, dealer, p_deck)
        elif split_cond(player, dealer):
            self.split(player, dealer, p_deck)
        else:
            return self.reg_play(player, dealer, p_deck)

        # for i in self.split_hand:
        #     if sum(i) <= 21:
        #         if sum(i) > sum(dealer):
        #             return sum(player), sum(dealer), self.split_hand[i], \
        #                    self.counter(self.count_holder, p_deck)
        #         elif sum(player) == sum(dealer):
        #             return sum(player), sum(dealer), 0, self.counter(self.count_holder, p_deck)
        #     return sum(player), sum(dealer), -self.split_hand[i], self.counter(self.count_holder, p_deck)

    # ##################################################################################################################

    def reg_play(self, player, dealer, deck):
        print("r")
        h_range = [0, 1, 7, 8, 9]
        # hit until 11 or more regardless of dealer hand
        while total(player) <= 11:
            self.hit(player, deck)
        # hit until 17 or more if dealer shows strong up card
        while total(player) <= 16 and (dealer[0] in h_range):
            self.hit(player, deck)
        # player busts
        if total(player) > 21:
            return total(player), total(dealer), -self.amount, round(self.counter(self.count_holder, deck), 5), \
                   len(deck)
        # dealer hits until 17 or more
        while total(dealer) < 17:
            self.hit(dealer, deck)
        # dealer busts
        if total(dealer) > 21:
            return total(player), total(dealer), self.amount, round(self.counter(self.count_holder, deck), 5), len(deck)
        # dealer doesn't bust, push
        elif total(dealer) == total(player):
            return total(player), total(dealer), 0, round(self.counter(self.count_holder, deck), 5), len(deck)
        # dealer doesn't bust, win
        elif total(dealer) > total(player):
            return total(player), total(dealer), -self.amount, round(self.counter(self.count_holder, deck), 5), \
                   len(deck)
        # dealer doesn't bust, lose
        elif total(player) > total(dealer):
            return total(player), total(dealer), self.amount, round(self.counter(self.count_holder, deck), 5), len(deck)

    # for splits and doubles
    def reg_play_dealer(self, player, dealer, deck):
        print("dealer only")
        while total(dealer) < 17:
            print(total(dealer), "dealer hit")
            self.hit(dealer, deck)
        # dealer busts
        if total(dealer) > 21:
            return total(player), total(dealer), self.amount, round(self.counter(self.count_holder, deck), 5), len(deck)
        # dealer doesn't bust, push
        elif total(dealer) == total(player):
            return total(player), total(dealer), 0, round(self.counter(self.count_holder, deck), 5), len(deck)
        # dealer doesn't bust, win
        elif total(dealer) > total(player):
            return total(player), total(dealer), -self.amount, round(self.counter(self.count_holder, deck), 5), \
                   len(deck)
        # dealer doesn't bust, lose
        elif total(player) > total(dealer):
            return total(player), total(dealer), self.amount, round(self.counter(self.count_holder, deck), 5), len(deck)

    def hit(self, hand: list, deck: list):
        if deck:
            card = deck.pop()
            self.count_holder.append(card)
            hand.append(card)
        else:
            self.new_game(deck)

    def new_game(self, deck):
        if not deck:
            exit()
        else:
            self.blackjack_game(deck)

    def counter(self, cards, deck):
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

        self.true_count += counter / (len(deck) + self.for_count)
        return self.true_count

    def blackjacks(self, player_hand, dealer_hand, deck):
        if (player_hand == [0, 1] or player_hand == [1, 0]) and (
                dealer_hand == [0, 1] or dealer_hand == [1, 0]):
            return total(player_hand), total(dealer_hand), 0, round(self.counter(self.count_holder, deck), 5), len(deck)

        elif (player_hand == [0, 1] or player_hand == [1, 0]) and (
                dealer_hand != [0, 1] or dealer_hand != [1, 0]):
            return total(player_hand), total(
                dealer_hand), self.amount * 1.5, round(self.counter(self.count_holder, deck), 5), len(deck)

        elif (player_hand != [0, 1] or player_hand != [1, 0]) and (
                dealer_hand == [0, 1] or dealer_hand == [1, 0]):
            return total(player_hand), total(
                dealer_hand), -self.amount, round(self.counter(self.count_holder, deck), 5), len(deck)

    def doubles(self, player_hand, dealer_hand, deck):
        # hard doubles
        if total(player_hand) == 11 or \
                (total(player_hand) == 10 and (
                        total(dealer_hand) in range(2, 10))) or \
                (total(player_hand) == 9 and (
                        total(dealer_hand) in range(3, 7))):

            self.hit(player_hand, deck)
            print("doubled")
            return True

        # soft doubles
        elif (1 in player_hand) and ((total(player_hand) == 19 and dealer_hand[0] == 6) or
                                     (total(player_hand) == 18 and dealer_hand[0] in range(3, 7)) or
                                     (total(player_hand) == 17 and dealer_hand[0] in range(2, 7)) or
                                     ((total(player_hand) == 16 or total(player_hand) == 15 or
                                       total(player_hand) == 14 or total(player_hand) == 13) and
                                      dealer_hand[0] in range(4, 7))):
            print("soft?", total(player_hand), player_hand)
            self.hit(player_hand, deck)
            return True
        print("undoubled")
        return False

    # note max split is 4 (4 hands)
    def split(self, hand, d_hand, deck):
        print("splits")
        if hand[0] == 1:  # aces can only take one hit after split and can only be split once
            self.split_hand[self.hit([1], deck)] = self.amount
            self.split_hand[self.hit([1], deck)] = self.amount
        else:
            while len(self.split_hand) <= 4:
                for i in hand:
                    self.split_hand[self.hit([i], deck)] = self.amount
                for j in self.split_hand:
                    if self.doubles(j, d_hand, deck):
                        self.split_hand[j] *= 2
                    elif split_cond(j, d_hand):
                        self.split(j, d_hand, deck)
                    else:
                        h_range = [0, 1, 7, 8, 9]
                        # keep hitting until player exceeds 16 when dealer shows 7 or higher for optimal play
                        while total(j) <= 16 and (d_hand[0] in h_range):
                            self.hit(j, deck)


#######################################################################################################################

tes = Game(8, 2, "c", 5, True)
decks = tes.setup()
print(tes.blackjack_game(decks))
