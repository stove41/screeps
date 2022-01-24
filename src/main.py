from collector import Collector
from builder import Builder
from defender import Defender
from harvester_new import HarvesterNew
# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

roles = ["collector", "builder", "defender", "harvester"]
role_counts = {"collector": 1,
               "builder": 1,
               "defender": 1,
               "harvester": 1}


class CreepSpawner:
    def __init__(self, spawn, num_creeps, role, sources):
        self.spawn = spawn
        self.num_creeps = num_creeps
        self.role = role
        self.sources = sources

    @staticmethod
    def get_part_cost(parts):
        cost_dict = {
            MOVE: 50,
            WORK: 100,
            CARRY: 50,
            ATTACK: 80,
            RANGED_ATTACK: 150,
            HEAL: 250,
            TOUGH: 10,
            CLAIM: 600
        }
        cost = 0
        for part in parts:
            cost += cost_dict[part]
        return cost

    def build_body(self):
        if self.role == "harvester":
            body = [WORK, WORK, MOVE]
            cost = self.get_part_cost(body)
            while cost <= self.spawn.room.energyAvailable and len(body) != 6:
                if self.spawn.room.energyAvailable - cost < 100:
                    return body
                else:
                    body.append(WORK)
                    cost = self.get_part_cost(body)
            return body
        elif self.role == "defender":
            body = [TOUGH, MOVE, ATTACK, MOVE, ATTACK, MOVE]
            return body
        else:
            body = [WORK, CARRY, MOVE]
            cost = self.get_part_cost(body)
            while cost <= self.spawn.room.energyAvailable:
                if self.spawn.room.energyAvailable - cost < 200:
                    return body
                else:
                    body.extend([WORK, CARRY, MOVE])
                    cost = self.get_part_cost(body)
            return body

    def spawn_creeps(self, body):
        if self.num_creeps < role_counts[self.role]:
            result = self.spawn.spawnCreep(body, "{}-{}".format(self.role, Game.time),
                                           {'memory': {'role': self.role}})
            console.log(JSON.stringify(result))

    def spawn_harvesters(self, body):
        if self.num_creeps < role_counts[self.role]:
            self.spawn.spawnCreep(body, "{}-{}".format(self.role, Game.time),
                                  {'memory': {'role': self.role, 'source': self.sources[self.num_creeps].id}})


def main():
    """
    Main game logic loop.
    """

    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.memory.role == "collector":
            Collector(creep).run_collector()
        elif creep.memory.role == "builder":
            Builder(creep).run_builder()
        elif creep.memory.role == "defender":
            Defender(creep).run_defender()
        elif creep.memory.role == "harvester":
            HarvesterNew(creep).run_harvester()

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        # Get Sources in spawn room.
        sources = spawn.room.find(FIND_SOURCES)
        if not spawn.spawning:
            for role in roles:
                # Get the number of <role> creeps in the room.
                num_creeps = _.sum(Game.creeps,
                                   lambda c: c.pos.roomName == spawn.pos.roomName and c.memory.role == role)
                # Instantiate spawner object.
                spawner = CreepSpawner(spawn, num_creeps, role, sources)
                if role == "harvester":
                    console.log(JSON.stringify(role))
                    body = spawner.build_body()
                    console.log(JSON.stringify(spawn.room.energyAvailable))
                    console.log(JSON.stringify(body))
                    spawner.spawn_harvesters(body)
                else:
                    console.log(JSON.stringify(role))
                    body = spawner.build_body()
                    console.log(JSON.stringify(spawn.room.energyAvailable))
                    console.log(JSON.stringify(body))
                    spawner.spawn_creeps(body)


module.exports.loop = main
