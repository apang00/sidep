from chooser import Chooser
from base import Game


#  Maybe make card counting a game function?


def run_game():
    games = []
    counter = 0
    i = Chooser()
    chosen = i.gather()
    decks = int(chosen[0])
    cut = float(chosen[1])
    style = chosen[2]
    amount = int(chosen[3])
    hands = int(chosen[4])
    count = True  # change later, right now it's a letter y or n

    while len(games) < hands:
        new_game = Game(decks, cut, style, amount, count)
        cut_deck = new_game.setup()

        while len(cut_deck) > 0:
            run_count = 0
            play = new_game.blackjack_game(cut_deck)
            #  normal game, no split, returns a tuple
            if type(play[0]) == int:
                run_count += play[3]
                # print(run_count)
                # print(len(cut_deck) / 52 + cut)
                play[3] = round(run_count / (len(cut_deck) / 52 + cut), 3)
                games.append(play)
                counter += 1
                cut_deck = cut_deck[-play[4]:]
                print("i")
            else:
                #  with split, it's a nested list
                cut_deck = cut_deck[-play[-1][-1]:]
                run_count += play[-1][3]
                for i in play:
                    # print(run_count)
                    # print(len(cut_deck) / 52 + cut)
                    i[3] = round(run_count / (len(cut_deck) / 52 + cut), 3)
                    counter += 1
                    games.append(i)

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
