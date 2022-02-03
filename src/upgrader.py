from defs import *
from base_creep import BaseCreep

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Upgrader(BaseCreep):
    def __init__(self, creep):
        super().__init__(creep)

    def run_upgrader(self):
        """
        Runs a creep as a generic harvester.
        :param creep: The creep to run
        """
        self.set_filling()
        if self.creep.memory.filling:
            # If we have a source use it
            if self.creep.memory.source:
                source = Game.getObjectById(self.creep.memory.source)
                if not source:
                    del self.creep.memory.source
            else:
                # Get location of the closest container or dropped resources.
                source = self.get_source("container")
                if source:
                    self.creep.memory.source = source.id
                else:
                    source = self.get_source("dropped")
                    if source:
                        self.creep.memory.source = source.id

            # If we're near the source, harvest it - otherwise, move to it.
            if self.creep.pos.isNearTo(source):
                self.collect_source(source)
                # result = self.creep.withdraw(source, RESOURCE_ENERGY)
                # if result != 0:
                #    self.creep.pickup(source)
            else:
                self.creep.moveTo(source)
        else:
            # If we have a saved target, use it
            if self.creep.memory.target:
                target = Game.getObjectById(self.creep.memory.target)
            else:
                target = self.get_target("controller")
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
                # if not self.creep.pos.inRangeTo(target, 2):
                #    self.creep.moveTo(target)
            else:
                self.creep.moveTo(target)
