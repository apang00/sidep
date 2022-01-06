# def tester(hand):
#     for i in hand:
#         if len(i) == 2 and i[0] == i[1] and len(hand) < 4:
#             a = [i[0]]
#             b = [i[1]]
#             hand.remove(i)
#             hand.append(a)
#             hand.append(b)
#             tester(hand)
#     return hand
#
#
# print(tester([[5, 5], [5, 5]]))

b = [1, 2, 6, 7]
b.sort(reverse=True)
print(b)
