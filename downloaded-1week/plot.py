# -*- coding: gbk -*-

import matplotlib.pyplot as plt

result = {3: 6902559, 33: 64, 6: 3116102, 12: 34393, 44: 105, 4: 3230357, 10: 483068, 13: 62259, 47: 33, 14: 19144, 7: 1839039, 11: 203725, 5: 5787243, 8: 628257, 17: 7177, 28: 256, 26: 229, 30: 130, 9: 176363, 42: 52, 18: 4812, 22: 498, 73: 3, 16: 3419, 24: 684, 2: 12369290, 50: 68, 39: 31, 48: 13, 15: 4168, 43: 66, 29: 722, 27: 1129, 35: 91, 21: 1889, 31: 118, 19: 2029, 45: 122, 36: 55, 54: 8, 60: 6, 46: 13, 53: 5, 25: 305, 56: 9, 20: 2011, 89: 1, 32: 100, 40: 50, 59: 5, 55: 5, 65: 4, 51: 16, 38: 212, 41: 68, 23: 1087, 68: 1, 70: 5, 37: 177, 52: 9, 49: 32, 62: 5, 34: 122, 72: 1, 57: 6, 64: 2, 88: 1, 79: 1, 61: 2, 58: 5, 75: 1, 63: 3, 80: 1, 102: 1, 77: 1, 1: 1136112}
result = {3: (124, 1174), 33: (38, 0), 6: (253, 720), 12: (480, 95), 44: (20, 0), 4: (177, 500), 10: (452, 148), 13: (376, 57), 47: (23, 0), 14: (264, 38), 7: (316, 204), 11: (457, 70), 5: (202, 260), 8: (407, 268), 17: (87, 8), 28: (59, 0), 26: (67, 0), 30: (54, 1), 9: (436, 143), 42: (32, 0), 18: (111, 4), 22: (45, 0), 73: (3, 0), 16: (100, 17), 24: (72, 0), 2: (34, 361), 50: (20, 0), 39: (21, 0), 48: (9, 0), 15: (152, 29), 43: (25, 0), 29: (47, 0), 27: (46, 0), 35: (29, 0), 21: (66, 0), 31: (46, 0), 19: (81, 3), 45: (21, 0), 36: (31, 0), 54: (6, 0), 60: (5, 0), 46: (12, 0), 53: (4, 0), 25: (65, 0), 56: (6, 0), 20: (59, 2), 89: (1, 0), 32: (45, 0), 40: (33, 0), 59: (5, 0), 55: (5, 0), 65: (4, 0), 51: (14, 0), 38: (36, 0), 41: (37, 0), 23: (67, 0), 68: (1, 0), 70: (3, 0), 37: (22, 0), 52: (9, 0), 49: (21, 0), 62: (5, 0), 34: (32, 0), 72: (1, 0), 57: (5, 0), 64: (2, 0), 88: (1, 0), 79: (1, 0), 61: (2, 0), 58: (3, 0), 75: (1, 0), 63: (3, 0), 80: (1, 0), 102: (1, 0), 77: (1, 0), 1: (1, 0)}
result = {3: (6805285, 97274), 33: (64, 0), 6: (3112907, 3195), 12: (34253, 140), 44: (105, 0), 4: (3224133, 6224), 10: (482732, 336), 13: (62180, 79), 47: (33, 0), 14: (19094, 50), 7: (1838437, 602), 11: (203614, 111), 5: (5785635, 1608), 8: (627778, 479), 17: (7164, 13), 28: (256, 0), 26: (229, 0), 30: (129, 1), 9: (175796, 567), 42: (52, 0), 18: (4805, 7), 22: (498, 0), 73: (3, 0), 16: (3398, 21), 24: (684, 0), 2: (12165671, 203619), 50: (68, 0), 39: (31, 0), 48: (13, 0), 15: (4137, 31), 43: (66, 0), 29: (722, 0), 27: (1129, 0), 35: (91, 0), 21: (1889, 0), 31: (118, 0), 19: (2026, 3), 45: (122, 0), 36: (55, 0), 54: (8, 0), 60: (6, 0), 46: (13, 0), 53: (5, 0), 25: (305, 0), 56: (9, 0), 20: (2009, 2), 89: (1, 0), 32: (100, 0), 40: (50, 0), 59: (5, 0), 55: (5, 0), 65: (4, 0), 51: (16, 0), 38: (212, 0), 41: (68, 0), 23: (1087, 0), 68: (1, 0), 70: (5, 0), 37: (177, 0), 52: (9, 0), 49: (32, 0), 62: (5, 0), 34: (122, 0), 72: (1, 0), 57: (6, 0), 64: (2, 0), 88: (1, 0), 79: (1, 0), 61: (2, 0), 58: (5, 0), 75: (1, 0), 63: (3, 0), 80: (1, 0), 102: (1, 0), 77: (1, 0), 1: (1136112, 0)}

def main():
    max_len = max(result.keys())
    max_len = 10
    xs = [i for i in range(1, max_len + 1)]
    ys = [result.get(x, (0, 0)) for x in xs]
    en_ys = [i[0] for i in ys]
    zh_ys = [i[1] for i in ys]
    _sum = sum(en_ys) + sum(zh_ys)
    en_ys = [y / _sum * 100 for y in en_ys]
    zh_ys = [y / _sum * 100 for y in zh_ys]
    xs = [str(i) for i in xs]
    plt.rcParams['font.sans-serif'] = 'kaiti'
    plt.figure()
    plt.plot(xs, en_ys, 'b:o', label = '????')
    plt.plot(xs, zh_ys, 'r:o', label = '????')
    plt.title('????????????', fontdict = {'family': 'kaiti'})
    plt.xlabel('??????????', loc = 'right', fontdict = {'family': 'kaiti'})
    plt.ylabel('?????????????? %', loc = 'top', fontdict = {'family': 'kaiti'})
    plt.grid(axis = 'y')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
