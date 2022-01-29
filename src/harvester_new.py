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
        # Set source from memory as source
        if self.creep.memory.source:
            source = Game.getObjectById(self.creep.memory.source)
        # If we're near the source, check for a container.
        if self.creep.pos.isNearTo(source):
            cont = self.creep.pos.findClosestByRange(FIND_STRUCTURES,
                                                     {"filter": lambda s:
                                                      s.structureType == STRUCTURE_CONTAINER})
            if cont:
                # If container is not within 3 spaces harvest source.
                if not self.creep.pos.isNearTo(cont, 3):
                    result = self.creep.harvest(source)
                else:
                    # If creep is on container, harvest source.
                    if self.creep.pos.isEqualTo(cont):
                        result = self.creep.harvest(source)
                    else:
                        # Else move to container
                        self.creep.moveTo(cont)
            else:
                # If container doesnt exist, harvest source.
                result = self.creep.harvest(source)
        # If not near source move to it.
        else:
            self.creep.moveTo(source)

