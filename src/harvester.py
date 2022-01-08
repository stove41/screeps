from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Harvester:
    def __init__(self, creep):
        self.creep = creep

    def get_source_terrain(self):
        return

    def run_harvester(self):
        """
        Runs a creep as a generic harvester.
        :param creep: The creep to run
        """

        # If we're full, stop filling up and remove the saved source
        if self.creep.memory.filling and self.creep.store.getFreeCapacity(RESOURCE_ENERGY) == 0:
            self.creep.memory.filling = False
            del self.creep.memory.source
        # If we're empty, start filling again and remove the saved target
        elif not self.creep.memory.filling and self.creep.carry.energy <= 0:
            self.creep.memory.filling = True
            del self.creep.memory.target

        if self.creep.memory.filling:
            # If we have a saved source, use it
            if self.creep.memory.source:
                source = Game.getObjectById(self.creep.memory.source)
            else:
                # Get a random new source and save it
                source = _(self.creep.room.find(FIND_SOURCES)).sample()
                if source:
                    self.creep.memory.source = source.id

            # If we're near the source, harvest it - otherwise, move to it.
            if self.creep.pos.isNearTo(source):
                result = self.creep.harvest(source)
                if result != OK:
                    print("[{}] Unknown result from creep.harvest({}): {}".format(self.creep.name, source, result))
            else:
                self.creep.moveTo(source)
        else:
            # If we have a saved target, use it
            if self.creep.memory.target:
                target = Game.getObjectById(self.creep.memory.target)
            else:
                # Get a new target.
                target = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                           {"filter": lambda s:
                                                            ((s.structureType == STRUCTURE_SPAWN
                                                             or s.structureType == STRUCTURE_EXTENSION)
                                                             and s.energy < s.energyCapacity)})
                if target:
                    self.creep.memory.target = target.id
                else:
                    target = self.creep.pos.findClosestByRange(FIND_MY_STRUCTURES,
                                                               {"filter": lambda s:
                                                                (s.structureType == STRUCTURE_CONTROLLER)})
                    if target:
                        self.creep.memory.target = target.id
                    else:
                        target = _(self.creep.room.find(FIND_STRUCTURES)) \
                            .filter(lambda s: (s.structureType == STRUCTURE_CONTROLLER)).sample()
                        self.creep.memory.target = target.id

            # If we are targeting a spawn or extension, we need to be directly next to it - otherwise, we can be 3 away.
            if target.energyCapacity:
                is_close = self.creep.pos.isNearTo(target)
            else:
                is_close = self.creep.pos.inRangeTo(target, 3)

            if is_close:
                # If we are targeting a spawn or extension, transfer energy. Otherwise, use upgradeController on it.
                if target.energyCapacity:
                    result = self.creep.transfer(target, RESOURCE_ENERGY)
                    if result == OK or result == ERR_FULL:
                        del self.creep.memory.target
                    else:
                        print("[{}] Unknown result from creep.transfer({}, {}): {}".format(
                            self.creep.name, target, RESOURCE_ENERGY, result))
                else:
                    result = self.creep.upgradeController(target)
                    if result != OK:
                        print("[{}] Unknown result from creep.upgradeController({}): {}".format(
                            self.creep.name, target, result))
                    # Let the creeps get a little closer than required to the controller, to make room for other creeps.
                    if not self.creep.pos.inRangeTo(target, 2):
                        self.creep.moveTo(target)
            else:
                self.creep.moveTo(target)
