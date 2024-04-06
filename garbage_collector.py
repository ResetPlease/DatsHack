import Interface
import config

STOP = 2

S = []
G = []


# def f(n, used, storage, garb_ids, garbage, X, Y, takearray):
#     if n == STOP:
#         S = storage
#         T = takearray
#     for id in garb_ids:
#         fig = garbage[id]
#         if not used[fig]:
#             for x in range(X):
#                 for y in range(Y):
#                     try:
#                         for dx in [1, -1, 1, -1]:
#                             for dy in [1, 1, -1, -1]:
#                                 if all([storage[x + dx*dot[0]][y + dy*dot[1]] == 0 for dot in fig]):
#
#                                     used[fig] = True
#                                     takearray.append(id)
#                                     for dot in fig:
#                                         storage[x + dx*dot[0]][y + dy*dot[1]] = id[-1]
#
#
#                                     f(n + 1, used, storage, garb_ids, garbage, X, Y)
#
#                                     used[fig] = False
#                                     for dot in fig:
#                                         storage[x + dx*dot[0]][y + dy*dot[1]] = 0
#
#                     except:
#                         pass
#

# naive_packer
def packer(X, Y, storage, garb_ids, garbage):
    ans = {}
    put = {}
    for id in garb_ids:
        fig = garbage[id]
        put[id] = False
        for x in range(X):
            for y in range(Y):

                for dx in [1, -1, 1, -1]:
                    for dy in [1, 1, -1, -1]:
                        if all(0 <= x + dx * dot[0] < X and 0 <= y + dy * dot[1] < Y for dot in fig):
                            if all([storage[x + dx * dot[0]][y + dy * dot[1]] == 0 for dot in fig]):
                                ans[id] = []
                                put[id] = True
                                for dot in fig:
                                    storage[x + dx * dot[0]][y + dy * dot[1]] = id
                                    ans[id].append([x + dx * dot[0], y + dy * dot[1]])

                        if put[id]: break
                    if put[id]: break
            if put[id]: break

    free_space = X * Y - sum([len(ans[fig_id]) for fig_id in ans])
    return ans, free_space


def pack_garbage():
    man = Interface(config.TOKEN)
    man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")
    universe = man.universe()
    garbage = universe["planet"]["garbage"] + universe["ship"]["garbage"]
    X, Y = universe["ship"]["capacityX", "capacityY"]

    garbage = {'2FyH43': [[0, 3], [1, 3], [2, 3], [2, 2], [2, 1], [3, 3], [3, 1], [3, 0]],
               '2HTbk3': [[0, 2], [0, 1], [0, 0], [1, 2], [1, 1]]}
    garb_to_collect = {}

    for piece in garbage:
        cnt = 0
        x = []
        y = []
        for coord in garbage[piece]:
            x.append(coord[0])
            y.append(coord[1])
            cnt += 1
        dx = max(x) - min(x)
        dy = max(y) - min(y)
        vol = dx * dy
        garb_to_collect[piece] = [vol * cnt]

    garb_to_collect = sorted(garb_to_collect.keys(), key=lambda x: x[1])
    storage = [[0 for i in range(Y)] for j in range(X)]
    ans = packer(X, Y, storage, garb_to_collect, garbage)

    return ans
