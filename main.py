from chooser import Chooser
from base import Game


#  Maybe make card counting a game function?
class Play:
    def __init__(self):
        self.results = []

    def run_game(self):
        i = Chooser()
        chosen = i.gather()
        decks = int(chosen[0])
        cut = float(chosen[1])
        style = chosen[2]
        amount = int(chosen[3])
        hands = int(chosen[4])
        count = True  # change later, right now it's a letter y or n
        game_counter = 0

        if style == "n":

            while len(self.results) < hands:
                new_game = Game(decks, cut, style, amount, count)
                cut_deck = new_game.setup()

                while len(cut_deck) > 0:

                    run_count = 0
                    play = new_game.blackjack_game(cut_deck)

                    #  normal game, no split, returns a tuple
                    if type(play[0]) == int:
                        if play[0] >= 30 or play[1] >= 30:
                            pass
                        else:
                            run_count += play[3]
                            play[3] = round(run_count / (len(cut_deck) / 52 + cut), 3)
                            self.results.append(play)
                            cut_deck = cut_deck[-play[4]:]

                    else:
                        #  with split, it's a nested list
                        cut_deck = cut_deck[-(play[-1][-1]):]
                        run_count += play[-1][3]
                        for i in play:
                            if i[0] >= 30 or i[1] >= 30:
                                pass
                            else:
                                i[3] = round(run_count / ((len(cut_deck) / 52) + cut), 3)
                                self.results.append(i)

            return self.results[0:hands]

        elif style == "m":

            while len(self.results) < hands:
                new_game = Game(decks, cut, style, amount, count)
                cut_deck = new_game.setup()
                bet_multi = 0
                player_win = True

                while len(cut_deck) > 0:
                    counter = 0
                    run_count = 0
                    play = new_game.blackjack_game(cut_deck)

                    #  normal game, no split, returns a tuple
                    if type(play[0]) == int:
                        if play[0] >= 30 or play[1] >= 30:
                            pass
                        else:
                            if not player_win:
                                play[2] = play[2] * bet_multi
                                print(bet_multi, play[2])
                            print(bet_multi, play[2])
                            run_count += play[3]
                            play[3] = round(run_count / (len(cut_deck) / 52 + cut), 3)
                            self.results.append(play)
                            game_counter += 1
                            if play[2] < 0:
                                if bet_multi == 0:
                                    bet_multi = 2
                                else:
                                    bet_multi *= 2
                                player_win = False

                            if play[2] > 0:
                                player_win = True
                                bet_multi = 0

                            cut_deck = cut_deck[-play[4]:]

                    else:
                        #  with split, it's a nested list
                        cut_deck = cut_deck[-(play[-1][-1]):]
                        run_count += play[-1][3]
                        print(bet_multi, "SPLITZ")
                        for i in play:
                            if i[0] >= 30 or i[1] >= 30:
                                pass
                            else:
                                if not player_win:
                                    print(bet_multi, i[2], "on loss")
                                    i[2] = i[2] * bet_multi
                                    if i[2] > 10000 or i[2] < -10000:
                                        print("OD")
                                print("on win")
                                i[3] = round(run_count / ((len(cut_deck) / 52) + cut), 3)
                                self.results.append(i)
                                game_counter += 1
                                counter += i[2]

                        if counter < 0:
                            if bet_multi == 0:
                                bet_multi = 2
                            else:
                                bet_multi *= 2
                            player_win = False
                        else:
                            player_win = True
                            bet_multi = 0

            # return self.results[0:hands]

        elif style == "o":

            while len(self.results) < hands:
                new_game = Game(decks, cut, style, amount, count)
                cut_deck = new_game.setup()

                while len(cut_deck) > 0:

                    run_count = 0
                    play = new_game.blackjack_game(cut_deck)

                    #  normal game, no split, returns a tuple
                    if type(play[0]) == int:
                        if play[0] >= 30 or play[1] >= 30:
                            pass
                        else:
                            run_count += play[3]
                            play[3] = round(run_count / (len(cut_deck) / 52 + cut), 3)
                            self.results.append(play)
                            game_counter += 1
                            cut_deck = cut_deck[-play[4]:]

                    else:
                        #  with split, it's a nested list
                        cut_deck = cut_deck[-(play[-1][-1]):]
                        run_count += play[-1][3]
                        for i in play:
                            if i[0] >= 30 or i[1] >= 30:
                                pass
                            else:
                                i[3] = round(run_count / ((len(cut_deck) / 52) + cut), 3)
                                self.results.append(i)
                                game_counter += 1

            return self.results[0:hands]

        elif style == "c":

            while len(self.results) < hands:
                new_game = Game(decks, cut, style, amount, count)
                cut_deck = new_game.setup()

                while len(cut_deck) > 0:

                    run_count = 0
                    play = new_game.blackjack_game(cut_deck)

                    #  normal game, no split, returns a tuple
                    if type(play[0]) == int:
                        if play[0] >= 30 or play[1] >= 30:
                            pass
                        else:
                            run_count += play[3]
                            play[3] = round(run_count / (len(cut_deck) / 52 + cut), 3)
                            self.results.append(play)
                            game_counter += 1
                            cut_deck = cut_deck[-play[4]:]

                    else:
                        #  with split, it's a nested list
                        cut_deck = cut_deck[-(play[-1][-1]):]
                        run_count += play[-1][3]
                        for i in play:
                            if i[0] >= 30 or i[1] >= 30:
                                pass
                            else:
                                i[3] = round(run_count / ((len(cut_deck) / 52) + cut), 3)
                                self.results.append(i)
                                game_counter += 1

            return self.results[0:hands]

a = Play()
print(a.run_game())
