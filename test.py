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


a = [3, -1, 0, 5, -1, -1]
a.sort(reverse=True)
print(a)
print(total(a))
