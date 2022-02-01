from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class BaseCreep:
    def __init__(self, creep):
        self.creep = creep

    def get_target(self, structure):
        if structure == "spawnstension":
            target = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                       {"filter": lambda s:
                                                        ((s.structureType == STRUCTURE_SPAWN
                                                         or s.structureType == STRUCTURE_EXTENSION
                                                         or s.structureType == STRUCTURE_TOWER)
                                                         and s.energy < s.energyCapacity)})
            return target

        elif structure == "controller":
            target = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                       {"filter": lambda s:
                                                        (s.structureType == STRUCTURE_CONTROLLER)})
            return target

    def get_source(self, type):
        if type == 'container':
            # Get location of closest container resources.
            source = self.creep.pos.findClosestByRange(FIND_STRUCTURES,
                                                       {"filter": lambda s:
                                                        (s.structureType == STRUCTURE_CONTAINER
                                                         and s.store.getUsedCapacity() >= 300)})
            '''TODO Make it so collectors find the largest amount of dropped resources first.'''
            return source
        elif type == "dropped":
            source = self.creep.pos.findClosestByRange(FIND_DROPPED_RESOURCES)
            return source

    def collect_source(self, source):
        result = self.creep.withdraw(source, RESOURCE_ENERGY)
        if result != 0:
            self.creep.pickup(source)

    def set_filling(self):
        # If we're full, stop filling up and remove the saved source
        if self.creep.memory.filling and self.creep.store.getFreeCapacity(RESOURCE_ENERGY) == 0:
            self.creep.memory.filling = False
            del self.creep.memory.source
        # If we're empty, start filling again and remove the saved target
        elif not self.creep.memory.filling and self.creep.carry.energy <= 0:
            self.creep.memory.filling = True
            del self.creep.memory.target

