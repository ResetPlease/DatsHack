import numpy as np
import random
from Interface import Interface
import config
import time
manager = Interface(config.TOKEN)
manager.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")

def ACO(distance_matrix, num_ants, max_iter, alpha, beta, rho):
    n = len(distance_matrix)
    pheromone = np.ones((n, n))  # Инициализация феромона

    best_path = None
    best_distance = float('inf')

    for iter in range(max_iter):
        ant_paths = []
        for ant in range(num_ants):
            visited = np.zeros(n, dtype=bool)
            path = [0]  # Начальная вершина всегда 0
            visited[0] = True

            while len(path) < n:
                current = path[-1]
                probs = np.zeros(n)
                possible_next_nodes = np.where(~visited)[0]  # Получаем индексы непосещенных вершин
                for next_node in possible_next_nodes:
                    if distance_matrix[current][next_node] != (1e12):
                        probs[next_node] = (pheromone[current][next_node] ** alpha) * ((1.0 / distance_matrix[current][next_node]) ** beta)
                if np.sum(probs) > 0:
                    probs /= np.sum(probs)  # Нормализуем вероятности
                else:
                    probs.fill(1 / len(probs))  # Если вероятности нулевые, устанавливаем равномерное распределение

                next = np.random.choice(n, p=probs)
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
                else:
                    pheromone[from_node][to_node] += -1

    return best_path, best_distance

def best_path(result):
    """
        universe is a data with planets and edges
    """
    nums = {}
    idx = 0
    names = {}
    for i in result:
        if i[0] not in nums:
            nums[i[0]] = idx
            names[idx] = i[0]
            idx+=1
        if i[1] not in nums:
            nums[i[1]] = idx
            names[idx] = i[0]
            idx+=1
    
    matrix = np.ones((len(nums), len(nums)))*(1e12)
    for i in result:
        u = nums[i[0]]
        v = nums[i[1]]
        w = i[2]
        matrix[u,v] = w
    # matrix = {}
    # for i in result:
    #     print(i)
    #     if i[0] in matrix:
    #         matrix[i[0]][i[1]] = i[2]
    #     else:
    #         matrix[i[0]] = {i[1] : i[2]}
    b, p = ACO(matrix, 10, 100, 1.0, 2.0, 0.5)
    print("Distance: ", p)
    r = []
    for i in b:
        r.append(names[i])
    return r
    

if __name__ == "__main__":
    start_time = time.time()
    data = manager.universe()
    result = data['universe']
    path = best_path(result)
    end_time = time.time()
    d = {}
    for i in result:
        print(i)
        if i[0] in d:
            d[i[0]].append(i[1])
        else:
            d[i[0]] = [i[1]]
    for i in range(len(path)-1):
        be = False
        for j in result:
            if j[0] == path[i] and j[1] == path[i+1]:
                be = True
                break
        if not be:
            print("NOT ", path[i], path[i+1])   
    print(path)
    print("Execution time:", end_time-start_time, "seconds")