from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Builder:
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
                nearest = self.creep.pos.findClosestByRange(FIND_STRUCTURES,
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
                    if nearest:
                        if self.creep.repair(nearest) == ERR_NOT_IN_RANGE:
                            self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
                    else:
                        # Get a new target.
                        target = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                                   {"filter": lambda s:
                                                                    (s.structureType == STRUCTURE_CONTROLLER)})
                        if target:
                            self.creep.memory.target = target.id

                        # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
                        is_close = self.creep.pos.inRangeTo(target, 3)

                        if is_close:
                            # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
                            result = self.creep.upgradeController(target)
                            if result != OK:
                                print("[{}] Unknown result from creep.upgradeController({}): {}".format(
                                    self.creep.name, target, result))
                        # Let the creeps get a little closer than required to the controller, to make room for other creeps.
                        if not self.creep.pos.inRangeTo(target, 2):
                            self.creep.moveTo(target)
                        else:
                            self.creep.moveTo(target)

        else:
            nearest = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                        {"filter": lambda s:
                                                         (s.structureType == STRUCTURE_EXTENSION and s.energy >= 50)
                                                         or (s.structureType == STRUCTURE_SPAWN and s.energy > 50)})
            if nearest:
                if self.creep.withdraw(nearest, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE:
                    self.creep.moveTo(nearest, {"visualizePathStyle": {"stroke": '#ff80ed'}})
                    result = self.creep.withdraw(nearest, RESOURCE_ENERGY)

