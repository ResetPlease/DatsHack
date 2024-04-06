from Interface import Interface
import config
import time
import numpy as np
from ACO import ACO
import heapq


man = Interface(config.TOKEN)
man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")
man.Register("travel", "https://datsedenspace.datsteam.dev/player/travel", "POST")
man.Register("reset", "https://datsedenspace.datsteam.dev/player/reset", "DELETE")


print(man.universe())

def dijkstra(graph, source, destination):
    shortest_paths = {source: (None, 0)}
    previous_nodes = {source: None}
    queue = [(0, source)]

    while queue:
        (dist, current_node) = heapq.heappop(queue)

        if current_node == destination:
            break

        for neighbor, weight in graph[current_node].items():
            old_dist = shortest_paths.get(neighbor, (None, float('inf')))[1]
            new_dist = dist + weight

            if new_dist < old_dist:
                shortest_paths[neighbor] = (current_node, new_dist)
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (new_dist, neighbor))

    path = []
    current_node = destination

    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    path.reverse()
    return path

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
            idx += 1
        if i[1] not in nums:
            nums[i[1]] = idx
            names[idx] = i[1]
            idx += 1

    matrix = np.ones((len(nums), len(nums))) * (1e12)
    for i in result:
        u = nums[i[0]]
        v = nums[i[1]]
        w = i[2]
        matrix[u, v] = w
    b, p = ACO(matrix, 10, 100, 1.0, 2.0, 0.5)
    print("Distance: ", p)
    r = []
    for i in b:
        r.append(names[i])
    return r


if __name__ == "__main__":
    start_time = time.time()
    data = man.universe()
    result = data['universe']
    path = best_path(result)
    end_time = time.time()
    print(path)
    print("Execution time:", end_time-start_time, "seconds")





# print(man.travel({"planets" : ["Moen"]}))


# result = man.universe()
# graph = {}
# result = result['universe']
# for i in result:
#     if i[0] in graph:
#         graph[i[0]][i[1]] = int(i[2])
#     else:
#         graph[i[0]] = {i[1] : i[2]}
#     print(*i, end=",\n")
