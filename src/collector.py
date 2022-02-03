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


class Collector(BaseCreep):
    def __init__(self, creep):
        super().__init__(creep)

    def run_collector(self):
        """
        Runs a creep as a generic harvester.
        :param creep: The creep to run
        """
        # set the filling variable in memory.
        self.set_filling()
        if self.creep.memory.filling:
            # If we have a source use it
            if self.creep.memory.source:
                source = Game.getObjectById(self.creep.memory.source)
                if not source:
                    del self.creep.memory.source
            else:
                # Get location of closest dropped resources.
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
                target = self.get_target("spawnstension")
                if target:
                    self.creep.memory.target = target.id
            # We need to be directly next to spawn or extension to transfer nrg.
            is_close = self.creep.pos.isNearTo(target)
            if is_close:
                # transfer energy
                if target.energyCapacity:
                    result = self.creep.transfer(target, RESOURCE_ENERGY)
                    if result == OK or result == ERR_FULL:
                        del self.creep.memory.target
                    else:
                        console.log(JSON.stringify(result))
            else:
                # If all nrg capacity is full move to out of the way spot.
                if self.creep.room.energyAvailable == self.creep.room.energyCapacityAvailable:
                    self.creep.moveTo(22, 6)
                else:
                    self.creep.moveTo(target)
