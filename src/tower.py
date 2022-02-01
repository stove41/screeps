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

    def run_tower(self):
        if len(self.tower.room.find(FIND_HOSTILE_CREEPS)) != 0:
            target = self.tower.pos.findClosestByRange(FIND_HOSTILE_CREEPS)
            result = self.tower.attack(target)
            console.log(JSON.stringify(result))
