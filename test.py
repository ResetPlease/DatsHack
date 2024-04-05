from Interface import Interface
import config


man = Interface(config.TOKEN)
man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")


print(man.universe())