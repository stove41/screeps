from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class HarvesterNew:
    def __init__(self, creep):
        self.creep = creep

    def get_source_terrain(self):
        return

    def run_harvester(self):
        """
        Runs a creep as a generic harvester.
        :param creep: The creep to run
        """
        # Find all sources.
        # Determine if a harvester is at the source.
        # If not, go to closest.
        if self.creep.memory.source:
            source = Game.getObjectById(self.creep.memory.source)
        # else:
        #    source = self.creep.pos.findClosestByRange(FIND_SOURCES)
        #    if source:
        #        self.creep.memory.source = source.id

        # If we're near the source, harvest it - otherwise, move to it.
        if self.creep.pos.isNearTo(source):
            cont = self.creep.pos.findClosestByRange(FIND_STRUCTURES,
                                                     {"filter": lambda s:
                                                      s.structureType == STRUCTURE_CONTAINER})
            if cont:
                if self.creep.pos.isEqualTo(cont):
                    result = self.creep.harvest(source)
                else:
                    res = self.creep.moveTo(cont)
                    console.log(JSON.stringify(res))
            else:
                result = self.creep.harvest(source)
        else:
            self.creep.moveTo(source)

