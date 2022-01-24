from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class Defender:
    def __init__(self, creep):
        self.creep = creep
        self.home

    def run_defender(self):
        if self.creep.memory.attacking and len(self.creep.room.find(FIND_HOSTILE_CREEPS)) == 0:
            self.creep.memory.attacking = False
            del self.creep.memory.target
            home = self.creep.pos.findClosestByPath(FIND_MY_SPAWNS)
            self.creep.memory.home = home.id
        elif self.creep.memory.attacking and self.creep.memory.target:
            target = Game.getObjectById(self.creep.memory.target)
            if self.creep.attack(target) == ERR_NOT_IN_RANGE:
                self.creep.moveTo(target, {"visualizePathStyle": {"stroke": '#7bf600'}})
        elif not self.creep.memory.attacking and self.creep.memory.home:
            home = Game.getObjectById(self.creep.memory.home)
            if self.creep.pos.isNearTo(home):
                del self.creep.memory.home
            self.creep.moveTo(home, {"visualizePathStyle": {"stroke": '#7bf600'}})
        else:
            if not self.creep.memory.attacking and len(self.creep.room.find(FIND_HOSTILE_CREEPS)) > 0:
                target = self.creep.pos.findClosestByPath(FIND_HOSTILE_CREEPS)
                self.creep.memory.target = target.id
                self.creep.memory.attacking = True


####
#### Need to fix bug where it gets stuck going between rooms where the are no enemies and so it delets the target from memory.
