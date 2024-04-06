from Interface import Interface
import config
import time
import numpy as np
from ACO import ACO
import heapq
from garbage_collector import pack_garbage

man = Interface(config.TOKEN)
man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")
man.Register("travel", "https://datsedenspace.datsteam.dev/player/travel", "POST")
man.Register("collect", "https://datsedenspace.datsteam.dev/player/collect", "POST")


print(man.universe())

def dijkstra(graph, source, destination):
    n = len(graph)
    distances = [float('inf')] * n
    previous_nodes = [None] * n
    distances[source] = 0

    queue = [(0, source)]

    while queue:
        (dist, current_node) = heapq.heappop(queue)

        if dist != distances[current_node]:
            continue

        for neighbor, weight in enumerate(graph[current_node]):
            if weight != 0:  # Ignore non-existent edges
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (new_dist, neighbor))

    path = []
    current_node = destination

    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    path.reverse()
    return path

def best_path(matrix, start):
    """
        universe is a data with planets and edges
    """

    b, p = ACO(matrix, 10, 50, 1.0, 2.0, 0.5, start=start)
    print("Distance: ", p)
    r = []
    for i in b:
        r.append(names[i])
    return b


if __name__ == "__main__":
    while(True):
        start_time = time.time()
        data = man.universe()
        cur = data["ship"]["planet"]["name"]
        result = data['universe']
        nums = {}
        idx = 0
        EDEN_IDX = 0
        names = {}
        for i in result:
            if i[0] not in nums:
                nums[i[0]] = idx
                if i[0] == "Eden":
                    EDEN_IDX = idx
                if i[0] == cur:
                    start = idx
                names[idx] = i[0]
                idx += 1
            if i[1] not in nums:
                if i[1] == "Eden":
                    EDEN_IDX = idx
                if i[1] == cur:
                    start = idx
                nums[i[1]] = idx
                names[idx] = i[1]
                idx += 1

        matrix = np.ones((len(nums), len(nums))) * (1e12)

        for i in result:
            u = nums[i[0]]
            v = nums[i[1]]
            w = i[2]
            matrix[u, v] = w


        path = best_path(matrix, start)[1:]
        end_time = time.time()
        print(path)
        print("Execution time:", end_time-start_time, "seconds")
        clear = []
        EMPTIED = False
        planet_garb = []
        ship_garb = []

        for i in range(len(path)):
            planet_num = path[i]
            if EMPTIED == False:
                travel = man.travel({"planets" : [names[planet_num]]})
                print(travel)
                planet_garb = travel["planetGarbage"]
                ship_garb = travel["shipGarbage"]
                time.sleep(0.25)
            if len(planet_garb) == 0:  # если остановились на пустой планете скип
                continue
            garb_config, storage_taken = pack_garbage(planet_garb, ship_garb)
            print(garb_config, storage_taken)
            if len(garb_config) != 0:
                collect_res = man.collect({"garbage" : garb_config})
                print(collect_res)
                time.sleep(0.25)
            EMPTIED = False
            # if len(collect_res["leaved"]) == 0:
            #     clear[planet_num] = True # сейчас не используется

            if storage_taken > 50:
                path_eden = dijkstra(matrix, planet_num, EDEN_IDX)
                path_back = dijkstra(matrix, EDEN_IDX, path[i+1])
                path_tot = path_eden[1:] + path_back[1:]
                path_req = []
                for p_num in path_tot:
                    path_req.append(names[p_num])

                i += 1
                EMPTIED = True
                travel = man.travel({"planets": path_req})
                print("------------------EMPTYING-------------")
                print(travel)
                print("---------------------------------------")
                planet_garb = travel["planetGarbage"]
                ship_garb = travel["shipGarbage"]
                storage_taken = 0
                time.sleep(0.25)








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
