import random

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


def smart_shuffle_with_probability(array, num_swaps, garbage):
    """
    Функция выполняет "умный" шаффл массива с учетом вероятности обмена элементов.

    :param array: Исходный массив.
    :param num_swaps: Количество шагов перемешивания.
    :return: Перемешанный массив.
    """
    # Копируем исходный массив, чтобы не изменять его
    shuffled_array = array.copy()

    # Выполняем заданное количество шагов перемешивания
    for _ in range(num_swaps):
        # Выбираем два случайных индекса
        index1, index2 = random.sample(range(len(shuffled_array)), 2)
        # Вычисляем разницу между элементами
        diff = abs(len(garbage[shuffled_array[index1]]) - len(garbage[shuffled_array[index2]]))
        # Вычисляем вероятность обмена на основе разницы
        probability = 1 - (diff / (max(shuffled_array) - min(shuffled_array) + 1))
        # Случайным образом решаем, следует ли обменять элементы
        if random.random() < probability:
            shuffled_array[index1], shuffled_array[index2] = shuffled_array[index2], shuffled_array[index1]

    return shuffled_array

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

    storage_taken_old = 0 if not ship_garbage else sum([len(ship_garbage[fig_id]) for fig_id in ship_garbage])
    ans, storage_taken = packer(X, Y, storage, garb_to_collect, garbage)

    # if storage_taken - storage_taken_old < 5:
    #     storage = [[0 for i in range(Y)] for j in range(X)]
    #     for id in ship_garbage.keys():  # Создаем список ключей для безопасной итерации
    #         for c in ship_garbage[id]:
    #             storage[c[0]][c[1]] = id
    #
    #     # Создаем копии словарей для безопасной модификации
    #     garb_to_collect_copy = garb_to_collect.copy()
    #     garbage_copy = garbage.copy()
    #
    #     for id in garb_to_collect_copy:
    #         if id in ship_garbage:
    #             garb_to_collect.remove(id)
    #
    #     for id in garbage_copy.keys():  # Используем список ключей для безопасной итерации
    #         if id in ship_garbage:
    #             del garbage[id]  # Используем del для удаления ключа из словаря
    #
    #     ans, storage_taken = packer(X, Y, storage, garb_to_collect, garbage)


    cnt = 0
    if storage_taken - storage_taken_old < 5:
        while storage_taken - storage_taken_old < 5 and cnt < 5:
            storage = [[0 for i in range(Y)] for j in range(X)]
            garb_to_collect = smart_shuffle_with_probability(garb_to_collect, 10)
            ans, storage_taken = packer(X, Y, storage, garb_to_collect, garbage)
            cnt += 1

    return ans, storage_taken
