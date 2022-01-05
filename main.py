from chooser import Chooser
from base import Game

games = []


def run_game():
    i = Chooser()
    chosen = i.gather()
    decks = int(chosen[0])
    cut = float(chosen[1])
    style = chosen[2]
    amount = int(chosen[3])
    count = True  # change later, right now it's a letter y or n

    new_game = Game(decks, cut, style, amount, count)
    cut_deck = new_game.setup()

    # print(new_game.blackjack_game(cut_deck))

    while len(cut_deck) > 0:
        play = new_game.blackjack_game(cut_deck)
        if type(play) == tuple:
            games.append(play)
            cut_deck = cut_deck[-play[4]:]
        else:
            cut_deck = cut_deck[-play[-1][-1]:]
            for i in play:
                games.append(i)
        print(games)
    return games

    # if style == "n":
    #     n = Game(decks, cut, "n", amount, count)
    # elif style == "m":
    #     m = Game(decks, cut, "m", amount, count)
    # elif style == "o":
    #     o = Game(decks, cut, "o", amount, count)
    # elif style == "c":
    #     c = Game(decks, cut, "c", amount, count)


def csv_extract(self):
    return self.results


# every betting pattern will return a list at the end
# ([hand #, player cards, dealer cards, W/L])

print(run_game())
