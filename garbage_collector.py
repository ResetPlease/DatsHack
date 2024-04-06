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
                '''
                + x + y
                - y + x
                - x - y
                + y - x
                '''
                for s in [1, -1]:
                    if all(0 <= x + s * dot[0] < X and 0 <= y + s * dot[1] < Y for dot in fig):
                        if all([storage[x + s * dot[0]][y + s * dot[1]] == 0 for dot in fig]):
                            ans[id] = []
                            put[id] = True
                            for dot in fig:
                                storage[x + s * dot[0]][y + s * dot[1]] = id
                                ans[id].append([x + s * dot[0], y + s * dot[1]])

                    # if put[id]: break

                    if not put[id] and all(0 <= x + s * dot[1] < X and 0 <= y - s * dot[0] < Y for dot in fig):
                        if all([storage[x + s * dot[1]][y - s * dot[0]] == 0 for dot in fig]):
                            ans[id] = []
                            put[id] = True
                            for dot in fig:
                                storage[x + s * dot[1]][y - s * dot[0]] = id
                                ans[id].append([x + s * dot[1], y - s * dot[0]])

                    if put[id]: break
            if put[id]: break

    storage_taken = sum([len(ans[fig_id]) for fig_id in ans])
    return ans, storage_taken


def normalize(fig):
    minx, miny = min([_[0] for _ in fig]), min([_[1] for _ in fig])
    return [[c[0] - minx, c[1] - miny] for c in fig]


def pack_garbage(garbage, ship_garbage):
    # man = Interface(config.TOKEN)
    # man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")
    # universe = man.universe()
    # garbage = universe["planet"]["garbage"] + universe["ship"]["garbage"]

    if ship_garbage is not None:
        for fig in ship_garbage:
            ship_garbage[fig] = normalize(ship_garbage[fig])
            garbage.update(ship_garbage)

    X, Y = 8, 11
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

    storage_taken_old = sum([len(ship_garbage[fig_id]) for fig_id in ship_garbage])
    ans, storage_taken = packer(X, Y, storage, garb_to_collect, garbage)

    if storage_taken - storage_taken_old < 5:
        storage = [[0 for i in range(Y)] for j in range(X)]
        for id in list(ship_garbage.keys()):  # Создаем список ключей для безопасной итерации
            for c in ship_garbage[id]:
                storage[c[0]][c[1]] = id

        # Создаем копии словарей для безопасной модификации
        garb_to_collect_copy = garb_to_collect.copy()
        garbage_copy = garbage.copy()

        for id in garb_to_collect_copy:  # Используем список ключей для безопасной итерации
            if id in ship_garbage:
                del garb_to_collect_copy[id]  # Используем del для удаления ключа из словаря

        for id in garbage_copy.keys():  # Используем список ключей для безопасной итерации
            if id in ship_garbage:
                del garbage_copy[id]  # Используем del для удаления ключа из словаря

        ans, storage_taken = packer(X, Y, storage, garb_to_collect_copy, garbage_copy)

    # if storage_taken - storage_taken_old < 5:
    #     for _ in range(5):
    #
    return ans
