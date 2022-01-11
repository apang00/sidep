# for if game is counted
import random


#######################################################################################################################
#######################################################################################################################
def total(hand):
    tot = 0
    for card in hand:
        if card == 0:
            tot += 10
        elif card == -1:
            if tot >= 11:
                tot += 1
            else:
                tot += 11
        else:
            tot += card
    return tot


def split_cond(player_hand, dealer_hand):
    if len(player_hand) == 2:
        if player_hand[0] == player_hand[1]:
            split_potential = True
        else:
            split_potential = False

        nine_split = [2, 3, 4, 5, 6, 8, 9]
        if split_potential and (((dealer_hand[0] in range(2, 8)) and
                                 (player_hand[0] == 2 or player_hand[0] == 3 or player_hand[0] == 7)) or
                                (player_hand[0] == 8 or player_hand[0] == -1) or
                                (dealer_hand[0] in range(5, 7) and (player_hand[0] == 4)) or
                                (dealer_hand[0] in range(2, 7) and (player_hand[0] == 6)) or
                                (dealer_hand[0] in nine_split and (player_hand[0] == 9))):
            return True
        return False
    else:
        return None
    # note: never split 5's or 10's for optimal play


#######################################################################################################################
#######################################################################################################################

def blackjack_cond(player, dealer):
    if (total(player) == 21 and len(player) == 2) or (total(dealer) == 21 and len(dealer) == 2):
        return True
    return False


def counter(cards):
    plus = [i for i in range(2, 7)]
    minus = [-1, 0]
    count = 0
    for i in cards:
        if i in plus:
            count += 1
        elif i in minus:
            count -= 1
        else:
            count += 0
    return count


class Game:

    def __init__(self, dex: int, cut: float, style: str, amount: int,
                 count: bool):

        self.decks = dex
        self.cut = cut
        self.count = count  # only if this is true is count_holder used

        self.style = style  # depending on if style is necessary
        self.amount = amount
        self.double = False

        self.split_hand = []
        self.count_holder = []

    def setup(self):
        deck = [-1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0] * 4 * self.decks  # normal deck
        random.shuffle(deck)
        return deck[int((52 * self.cut)):]

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
            self.double = True
            return self.reg_play_dealer(player, dealer, p_deck)
        elif split_cond(player, dealer):
            return self.split(player, dealer, p_deck)
        else:
            return self.reg_play(player, dealer, p_deck)

    # ##################################################################################################################
    # note max split is 4 (4 hands)
    def more_split(self, hand):
        for i in hand:
            if len(i) == 2 and i[0] == i[1] and len(hand) < 4:
                a = [i[0]]
                b = [i[1]]
                hand.remove(i)
                hand.append(a)
                hand.append(b)
                self.more_split(hand)
        return hand

    def split_helper(self, hand, deck):
        hand = [[hand[0]], [hand[1]]]
        for i in hand:
            self.hit(i, deck)
        return self.more_split(hand)

    def split(self, hand, d_hand, deck):
        # print("splits", hand[0])
        if hand[0] == -1:  # aces can only take one hit after split and can only be split once
            hand = [[-1], [-1]]
            for i in hand:
                self.hit(i, deck)
            for j in hand:
                self.split_hand.append(self.reg_play_dealer(j, d_hand, deck))
            return self.split_hand
        else:
            new_hand = self.split_helper(hand, deck)
            for i in new_hand:
                if len(i) == 1:
                    self.hit(i, deck)
            for i in new_hand:
                if self.doubles(i, d_hand, deck):
                    self.double = True
                    self.split_hand.append(self.reg_play_dealer(i, d_hand, deck))
                else:
                    self.split_hand.append(self.reg_play(i, d_hand, deck))
        return self.split_hand

    def reg_play(self, player, dealer, deck):
        # print("r")
        h_range = [0, -1, 7, 8, 9]
        # hit until 11 or more regardless of dealer hand
        while total(player) <= 11:
            self.hit(player, deck)
            # print(total(player))
        # hit until 17 or more if dealer shows strong up card
        while total(player) <= 16 and (dealer[0] in h_range):
            self.hit(player, deck)
        # player busts
        if total(player) > 21:
            return [total(player), total(dealer), -self.amount, counter(self.count_holder), len(deck)]
        # dealer hits until 17 or more
        while total(dealer) < 17:
            # print(total(dealer), "hit")
            self.hit(dealer, deck)
        # dealer busts
        if total(dealer) > 21:
            return [total(player), total(dealer), self.amount, counter(self.count_holder), len(deck)]
        # dealer doesn't bust, push
        elif total(dealer) == total(player):
            return [total(player), total(dealer), 0, counter(self.count_holder), len(deck)]
        # dealer doesn't bust, win
        elif total(dealer) > total(player):
            return [total(player), total(dealer), -self.amount, counter(self.count_holder), len(deck)]
        # dealer doesn't bust, lose
        elif total(player) > total(dealer):
            return [total(player), total(dealer), self.amount, counter(self.count_holder), len(deck)]

    # for splits and doubles
    def reg_play_dealer(self, player, dealer, deck):
        # print("dealer only")
        while total(dealer) < 17:
            # print(total(dealer), "dealer hit")
            self.hit(dealer, deck)
        # dealer busts
        if total(dealer) > 21 and self.double:
            self.double = False
            return [total(player), total(dealer), self.amount * 2, counter(self.count_holder), len(deck)]
        elif total(dealer) > 21 and not self.double:
            return [total(player), total(dealer), self.amount, counter(self.count_holder), len(deck)]
        # dealer doesn't bust, push
        elif total(dealer) == total(player):
            return [total(player), total(dealer), 0, counter(self.count_holder), len(deck)]
        # dealer doesn't bust, win
        elif total(dealer) > total(player) and self.double:
            self.double = False
            return [total(player), total(dealer), -(self.amount * 2), counter(self.count_holder), len(deck)]
        elif total(dealer) > total(player) and not self.double:
            return [total(player), total(dealer), -self.amount, counter(self.count_holder), len(deck)]
        # dealer doesn't bust, lose
        elif total(player) > total(dealer) and self.double:
            self.double = False
            return [total(player), total(dealer), self.amount * 2, counter(self.count_holder), len(deck)]
        elif total(player) > total(dealer) and not self.double:
            return [total(player), total(dealer), self.amount, counter(self.count_holder), len(deck)]

    def hit(self, hand: list, deck: list):
        if deck:
            card = deck.pop()
            self.count_holder.append(card)
            hand.append(card)
            hand.sort(reverse=True)
        else:
            for i in range(3):
                hand.append(0)

    def blackjacks(self, player_hand, dealer_hand, deck):
        if (player_hand == [0, -1] or player_hand == [-1, 0]) and (
                dealer_hand == [0, -1] or dealer_hand == [-1, 0]):
            # print("blkjk")
            return [total(player_hand), total(dealer_hand), 0, counter(self.count_holder), len(deck)]

        elif (player_hand == [0, -1] or player_hand == [-1, 0]) and (
                dealer_hand != [0, -1] or dealer_hand != [-1, 0]):
            # print("blkjk")
            return [total(player_hand), total(
                dealer_hand), self.amount * 1.5, counter(self.count_holder), len(deck)]

        elif (player_hand != [0, -1] or player_hand != [-1, 0]) and (
                dealer_hand == [0, -1] or dealer_hand == [-1, 0]):
            return [total(player_hand), total(
                dealer_hand), -self.amount, counter(self.count_holder), len(deck)]

    def doubles(self, player_hand, dealer_hand, deck):
        # hard doubles
        if total(player_hand) == 11 or \
                (total(player_hand) == 10 and (
                        total(dealer_hand) in range(2, 10))) or \
                (total(player_hand) == 9 and (
                        total(dealer_hand) in range(3, 7))):
            # print("hard double", total(player_hand))
            self.hit(player_hand, deck)
            return True

        # soft doubles
        elif (-1 in player_hand) and ((total(player_hand) == 19 and dealer_hand[0] == 6) or
                                      (total(player_hand) == 18 and dealer_hand[0] in range(3, 7)) or
                                      (total(player_hand) == 17 and dealer_hand[0] in range(2, 7)) or
                                      ((total(player_hand) == 16 or total(player_hand) == 15 or
                                        total(player_hand) == 14 or total(player_hand) == 13) and
                                       dealer_hand[0] in range(4, 7))):
            # print("soft double", total(player_hand))
            self.hit(player_hand, deck)
            # print(total(player_hand))
            return True
        # print("no double")
        return False

#######################################################################################################################

# tes = Game(8, 2, "c", 10, True)
# decks = tes.setup()
# print(tes.blackjack_game(decks))
