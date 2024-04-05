from Interface import Interface
import config


man = Interface(config.TOKEN)
man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")
man.Register("travel", "https://datsedenspace.datsteam.dev/player/travel", "POST")

print(man.travel({"planets" : ["Moen"]}))


# result = man.universe()
# graph = {}
# result = result['universe']
# for i in result:
#     if i[0] in graph:
#         graph[i[0]][i[1]] = int(i[2])
#     else:
#         graph[i[0]] = {i[1] : i[2]}
#     print(*i, end=",\n")
