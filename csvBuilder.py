import csv
from chooser import Chooser

with open('data', 'w', newline='') as f:
    forR = csv.writer(f)

    forR.writerow(["Games Played", "Player Hand", "Dealer Hand", "Win/Loss ($)",
                   "Count"])

    c = Chooser()
    data = c.gather()
    game = Play(data[0], data[1], data[2], data[3], data[4]) # play no longer a class... modify this

    game.run_game()
    forCsv = game.csv_extract()
    for i in forCsv:
        forR.writerow([i[0], i[1], i[2], i[3], i[4]])
    # take returns from bet patterns and build csv


