from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def run_builder(creep):
    if creep.memory.building and creep.store[RESOURCE_ENERGY] == 0:
        creep.memory.building = False
        creep.say('collect')

    if not creep.memory.building and creep.store.getFreeCapacity() == 0:
        creep.memory.building = True
        creep.say('build')

    if creep.memory.building:
        nearest = creep.pos.findClosestByRange(FIND_CONSTRUCTION_SITES)
        if creep.build(nearest) == ERR_NOT_IN_RANGE:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffffff'}})
    else:
        # console.log("else clause")
        # creep.memory.building = True
        nearest = creep.pos.findClosestByRange(FIND_MY_SPAWNS)

           # _.filter(creep.room.find(FIND_STRUCTURES),
           #          lambda x: (x.structureType == STRUCTURE_CONTAINER or
           #                     x.structureType == STRUCTURE_STORAGE or
           #                     x.structureType == STRUCTURE_SPAWN) and
           #                    x.store.getUsedCapacity() > 0))
        #  print(creep, "builder", nearest)
        try:
            result = creep.withdraw(nearest, RESOURCE_ENERGY)
        except:
            creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})


        # if creep.withdraw(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
        #    creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ffaa00'}})
        #    result = creep.withdraw(nearest, RESOURCE_ENERGY)
        #    console.log(JSON.stringify(result))