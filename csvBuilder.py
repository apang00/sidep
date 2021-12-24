import csv

with open('data', 'w', newline='') as f:
    forR = csv.writer(f)

    forR.writerow(["Games Played", "Player Hand", "Dealer Hand", "Win/Loss"])
    # take returns from bet patterns and build csv

