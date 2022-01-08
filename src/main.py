from harvester import Harvester
from builder import Builder
from defender import Defender
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

roles = ["harvester", "builder", "defender"]
role_counts = {"harvester": 12,
               "builder": 2,
               "defender": 1}
role_bodies = {"harvester": [WORK, CARRY, MOVE, MOVE],
               "builder": [WORK, CARRY, MOVE, MOVE],
               "defender": [TOUGH, MOVE, ATTACK, MOVE]}
high_nrg_bodies = {"harvester": [WORK, CARRY, CARRY, MOVE, MOVE, MOVE],
                   "builder": [WORK, CARRY, CARRY, MOVE, MOVE, MOVE],
                   "defender": [TOUGH, MOVE, ATTACK, MOVE, ATTACK, MOVE]}


def main():
    """
    Main game logic loop.
    """
    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.memory.role == "harvester":
            Harvester(creep).run_harvester()
        elif creep.memory.role == "builder":
            Builder(creep).run_builder()
        elif creep.memory.role == "defender":
            Defender(creep).run_defender()

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            for role in roles:
                # Get the number of our creeps in the room.
                num_creeps = _.sum(Game.creeps,
                                   lambda c: c.pos.roomName == spawn.pos.roomName and c.memory.role == role)
                # If there are no creeps, spawn a creep once energy is at 250 or more
                if num_creeps <= 0 and spawn.room.energyAvailable >= 250 and role != "defender":
                    spawn.spawnCreep(role_bodies[role], "{}-{}".format(role, Game.time),
                                     {'memory': {'role': role}})
                # If there are less than role_count creeps but at least one,
                # wait until 350 nrg for bigger body.
                elif num_creeps < role_counts[role] and spawn.room.energyAvailable >= 350:
                    spawn.spawnCreep(high_nrg_bodies[role], "{}-{}".format(role, Game.time),
                                     {'memory': {'role': role}})
                # Else spawn a small creep
                #elif num_creeps < role_counts[role] and spawn.room.energyAvailable >= 250:
                #    spawn.spawnCreep(role_bodies[role], "{}-{}".format(role, Game.time),
                #                     {'memory': {'role': role}})


module.exports.loop = main
