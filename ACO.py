import numpy as np
import random
from Interface import Interface
import config
import time
manager = Interface(config.TOKEN)
manager.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")

def ACO(distance_matrix, num_ants, max_iter, alpha, beta, rho, start):
    n = len(distance_matrix)
    pheromone = np.zeros((n, n))  # Инициализация феромона
    for i in range(n):
        for j in range(n):
            if distance_matrix[i][j] != 1e12:
                pheromone[i][j] = 1

    best_path = None
    best_distance = float('inf')

    for iter in range(max_iter):
        ant_paths = []
        for ant in range(num_ants):
            visited = np.zeros(n, dtype=bool)
            path = [start]
            visited[start] = True

            while len(path) < n:
                current = path[-1]
                neighbors = []
                for i in range(n):
                    if (i != current) and distance_matrix[current][i] != 1e12:
                        neighbors.append(i)
                probs = np.zeros(len(neighbors))
                possible_next_nodes = np.where(~visited)[0]  # Получаем индексы непосещенных вершин
                for i in range(len(neighbors)):
                    if visited[neighbors[i]] == 0:
                        probs[i] = (pheromone[current][neighbors[i]] ** alpha) * ((1.0 / distance_matrix[current][neighbors[i]]) ** beta)

                # for next_node in possible_next_nodes:
                #     if distance_matrix[current][next_node] != (1e12):
                #         probs[next_node] = (pheromone[current][next_node] ** alpha) * ((1.0 / distance_matrix[current][next_node]) ** beta)
                if np.sum(probs) > 0:
                    probs /= np.sum(probs)  # Нормализуем вероятности
                else:
                    probs.fill(1 / len(probs))  # Если вероятности нулевые, устанавливаем равномерное распределение

                next = np.random.choice(neighbors, p=probs)
                path.append(next)
                visited[next] = True

            ant_paths.append(path)

        # Обновление феромона
        for i in range(num_ants):
            distance = sum(distance_matrix[ant_paths[i][j]][ant_paths[i][j + 1]] for j in range(n - 1))
            distance += distance_matrix[ant_paths[i][-1]][0]  # Добавляем расстояние до начальной вершины
            if distance < best_distance:
                best_path = ant_paths[i]
                best_distance = distance

        pheromone *= (1 - rho)  # Испарение феромона

        for i in range(num_ants):
            for j in range(n - 1):
                from_node, to_node = ant_paths[i][j], ant_paths[i][j + 1]
                if distance_matrix[from_node][to_node] != 1e12:  # Проверяем наличие ребра
                    pheromone[from_node][to_node] += 1.0 / best_distance

    return best_path, best_distance

# def best_path(result):
#     """
#         universe is a data with planets and edges
#     """
#     nums = {}
#     idx = 0
#     names = {}
#     for i in result:
#         if i[0] not in nums:
#             nums[i[0]] = idx
#             names[idx] = i[0]
#             idx+=1
#         if i[1] not in nums:
#             nums[i[1]] = idx
#             names[idx] = i[1]
#             idx+=1
#
#     matrix = np.ones((len(nums), len(nums)))*(1e12)
#     for i in result:
#         u = nums[i[0]]
#         v = nums[i[1]]
#         w = i[2]
#         matrix[u,v] = w
#     # matrix = {}
#     # for i in result:
#     #     print(i)
#     #     if i[0] in matrix:
#     #         matrix[i[0]][i[1]] = i[2]
#     #     else:
#     #         matrix[i[0]] = {i[1] : i[2]}
#     b, p = ACO(matrix, 10, 100, 1.0, 2.0, 0.5, start=start)
#     print("Distance: ", p)
#     r = []
#     for i in b:
#         r.append(names[i])
#     return b
#
#
# if __name__ == "__main__":
#     start_time = time.time()
#     data = manager.universe()
#     result = data['universe']
#     path = best_path(result)
#     end_time = time.time()
#     d = {}
#     for i in result:
#         print(i)
#         if i[0] in d:
#             d[i[0]].append(i[1])
#         else:
#             d[i[0]] = [i[1]]
#     for i in range(len(path)-1):
#         be = False
#         for j in result:
#             if j[0] == path[i] and j[1] == path[i+1]:
#                 be = True
#                 break
#         if not be:
#             print("NOT ", path[i], path[i+1])
#     print(path)
#     print("Execution time:", end_time-start_time, "seconds")