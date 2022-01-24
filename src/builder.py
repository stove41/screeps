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

        if not self.creep.memory.building and self.creep.store.getFreeCapacity() == 0:
            self.creep.memory.building = True

        if self.creep.memory.building:
            nearest = self.creep.pos.findClosestByRange(FIND_MY_CONSTRUCTION_SITES)
            if nearest:
                if self.creep.build(nearest) == ERR_NOT_IN_RANGE:
                    self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
            else:
                nearest = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                            {"filter": lambda s:
                                                             ((s.structureType == STRUCTURE_WALL and s.hits <= 50000)
                                                              or (s.structureType == STRUCTURE_RAMPART and s.hits <= 50000)
                                                              or s.structureType == STRUCTURE_ROAD
                                                              and s.hits < s.hitsMax)})
                if nearest:
                    if self.creep.repair(nearest) == ERR_NOT_IN_RANGE:
                        self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
                else:
                    nearest = self.creep.pos.findClosestByRange(FIND_STRUCTURES,
                                                                {"filter": lambda s:
                                                                 (s.structureType == STRUCTURE_CONTAINER
                                                                  and s.hits < s.hitsMax)})
                    if self.creep.repair(nearest) == ERR_NOT_IN_RANGE:
                        self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})

        else:
            nearest = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                        {"filter": lambda s:
                                                         (s.structureType == STRUCTURE_EXTENSION and s.energy >= 50)
                                                         or (s.structureType == STRUCTURE_SPAWN and s.energy > 50)})
            if self.creep.withdraw(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
                self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
                result = self.creep.withdraw(nearest, RESOURCE_ENERGY)
