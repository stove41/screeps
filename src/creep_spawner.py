from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


class CreepSpawner:
    """Class definition for creep spawner containing functions used while spawning creeps.
        spawn: the current spawn from Game.spawns
        num_creeps: the number of <role> creeps present in the room.
        role: The current role.
        last_source_idx: The index of the last source a harvester was sent to."""
    def __init__(self, spawn, num_creeps, role):
        self.spawn = spawn
        self.num_creeps = num_creeps
        self.role = role

    def get_source(self):
        """Method to find all sources in a room and assign the correct one to the currently spawning harvester."""
        sources = self.spawn.room.find(FIND_SOURCES)
        if self.num_creeps == 0:
            source = sources[0]
            self.spawn.memory.last_idx = 0
            return source.id, self.spawn.memory.last_idx
        elif self.num_creeps != 0 and self.spawn.memory.last_idx == 0:
            source = sources[1]
            self.spawn.memory.last_idx = 1
            return source.id, self.spawn.memory.last_idx
        elif self.num_creeps != 0 and self.spawn.memory.last_idx == 1:
            source = sources[0]
            self.spawn.memory.last_idx = 0
            return source.id, self.spawn.memory.last_idx

    @staticmethod
    def get_part_cost(parts):
        """Method to calculate the cost of bodies while building them."""
        cost_dict = {
            MOVE: 50,
            WORK: 100,
            CARRY: 50,
            ATTACK: 80,
            RANGED_ATTACK: 150,
            HEAL: 250,
            TOUGH: 10,
            CLAIM: 600
        }
        cost = 0
        for part in parts:
            cost += cost_dict[part]
        return cost

    def build_defender(self):
        body = [TOUGH, MOVE, ATTACK, MOVE, ATTACK, MOVE]
        return body

    def build_builder(self):
        body = [WORK, CARRY, MOVE, MOVE]
        cost = self.get_part_cost(body)
        while cost <= self.spawn.room.energyAvailable:
            if self.spawn.room.energyAvailable - cost < 300:
                return body
            else:
                body.extend([WORK, CARRY, MOVE, MOVE])
                cost = self.get_part_cost(body)
        return body

    def build_upgrader(self):
        body = [WORK, CARRY, MOVE, MOVE]
        cost = self.get_part_cost(body)
        while cost <= self.spawn.room.energyAvailable:
            if self.spawn.room.energyAvailable - cost < 250:
                return body
            else:
                body.extend([WORK, CARRY, MOVE, MOVE])
                cost = self.get_part_cost(body)
        return body

    def build_collector(self):
        body = [CARRY, CARRY, MOVE, MOVE]
        cost = self.get_part_cost(body)
        while cost <= self.spawn.room.energyAvailable:
            if self.spawn.room.energyAvailable - cost < 250:
                return body
            else:
                body.extend([CARRY, CARRY, MOVE, MOVE])
                cost = self.get_part_cost(body)
        return body

    def build_harvester(self):
        body = [WORK, WORK, MOVE]
        cost = self.get_part_cost(body)
        while cost <= self.spawn.room.energyAvailable and len(body) != 6:
            if self.spawn.room.energyAvailable - cost < 100:
                return body
            else:
                body.append(WORK)
                cost = self.get_part_cost(body)
        return body

    def spawn_creeps(self, body):
        self.spawn.spawnCreep(body, "{}-{}".format(self.role, Game.time),
                              {'memory': {'role': self.role}})

    def spawn_harvesters(self, body):
        source, idx = self.get_source()
        self.spawn.memory.last_idx = idx
        self.spawn.spawnCreep(body, "{}-{}".format(self.role, Game.time),
                              {'memory': {'role': self.role, 'source': source}})
        return idx
