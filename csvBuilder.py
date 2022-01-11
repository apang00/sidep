import csv
from main import Play

holder = []


def get_data():
    game = Play()
    data = game.run_game()
    return data


def build_csv(data):
    counter = 0
    with open('data3.csv', 'w', newline='') as f:
        forR = csv.writer(f)

        forR.writerow(["Games Played", "Player Hand", "Dealer Hand", "Win/Loss ($)",
                       "Count"])
        for i in data:
            counter += 1
            forR.writerow([counter, i[0], i[1], i[2], i[3]])

    # take returns from bet patterns and build csv


a = get_data()
build_csv(a)
