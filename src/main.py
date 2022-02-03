from collector import Collector
from builder import Builder
from defender import Defender
from harvester_new import HarvesterNew
from upgrader import Upgrader
from creep_spawner import CreepSpawner
from tower import Tower
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

roles = ["collector", "builder", "defender", "harvester", "upgrader"]
role_counts = {"collector": 2,
               "builder": 2,
               "defender": 1,
               "harvester": 2,
               "upgrader": 1}


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
        elif creep.memory.role == "upgrader":
            Upgrader(creep).run_upgrader()

    # Run each tower
    towers = _.filter(Game.structures,
                      lambda s: s.structureType == STRUCTURE_TOWER)
    for name in towers:
        tower = Game.structures[name.id]
        Tower(tower).run_tower()

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            for role in roles:
                # Get the number of <role> creeps in the room.
                num_creeps = _.sum(Game.creeps,
                                   lambda c: c.pos.roomName == spawn.pos.roomName and c.memory.role == role)
                # Instantiate spawner object.
                spawner = CreepSpawner(spawn, num_creeps, role)
                if role == "harvester":
                    if num_creeps < role_counts[role] and spawn.room.energyAvailable > 250:
                        body = spawner.build_harvester()
                        idx = spawner.spawn_harvesters(body)
                        last_idx = idx
                elif role == "defender":
                    if num_creeps < role_counts[role] and spawn.room.energyAvailable > 320:
                        body = spawner.build_defender()
                        spawner.spawn_creeps(body)
                elif role == "collector":
                    if num_creeps < role_counts[role] and spawn.room.energyAvailable > 250:
                        body = spawner.build_collector()
                        spawner.spawn_creeps(body)
                elif role == "upgrader":
                    if num_creeps < role_counts[role] and spawn.room.energyAvailable > 250:
                        body = spawner.build_upgrader()
                        spawner.spawn_creeps(body)
                elif role == "builder":
                    if num_creeps < role_counts[role] and spawn.room.energyAvailable > 250:
                        body = spawner.build_builder()
                        spawner.spawn_creeps(body)


module.exports.loop = main
