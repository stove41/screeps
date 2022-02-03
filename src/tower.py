from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Tower:
    def __init__(self, tower):
        self.tower = tower

    def get_target(self):
        target = self.tower.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
        return target

    def find_repairs(self):
        nearest = self.tower.pos.findClosestByRange(FIND_STRUCTURES,
                                                    {"filter": lambda s:
                                                    ((s.structureType == STRUCTURE_WALL and s.hits <= 50000)
                                                     or (s.structureType == STRUCTURE_RAMPART and s.hits <= 50000)
                                                     or s.structureType == STRUCTURE_ROAD
                                                     and s.hits < s.hitsMax)})
        return nearest

    def find_wounded(self):
        wounded_creeps = self.tower.room.find(FIND_MY_CREEPS,
                                              {"filter": lambda s:
                                               s.hits / s.hitsMax <= 0.55})
        return wounded_creeps

    def run_tower(self):
        if len(self.tower.room.find(FIND_HOSTILE_CREEPS)) != 0:
            target = self.get_target()
            self.tower.attack(target)
        wounded_creeps = self.find_wounded()
        if len(wounded_creeps) > 0:
            for creep in wounded_creeps:
                self.tower.heal(creep)
        nearest = self.find_repairs()
        if len(nearest) > 0:
            self.tower.repair(nearest)

