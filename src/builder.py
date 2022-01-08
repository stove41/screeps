from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Builder():
    def __init__(self, creep):
        self.creep = creep

    def run_builder(self):
        if self.creep.memory.building and self.creep.store[RESOURCE_ENERGY] == 0:
            self.creep.memory.building = False
            self.creep.say('collect')

        if not self.creep.memory.building and self.creep.store.getFreeCapacity() == 0:
            self.creep.memory.building = True
            self.creep.say('build')

        if self.creep.memory.building:
            nearest = self.creep.pos.findClosestByRange(FIND_CONSTRUCTION_SITES)
            if self.creep.build(nearest) == ERR_NOT_IN_RANGE:
                self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
        else:
            nearest = self.creep.pos.findClosestByRange(FIND_MY_SPAWNS)
            if self.creep.withdraw(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
                self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
                result = self.creep.withdraw(nearest, RESOURCE_ENERGY)
