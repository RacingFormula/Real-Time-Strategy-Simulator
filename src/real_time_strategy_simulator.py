import numpy as np
import time

class Unit:
    def __init__(self, id, team, position, health, attack_power, range):
        self.id = id
        self.team = team
        self.position = np.array(position)
        self.health = health
        self.attack_power = attack_power
        self.range = range

    def is_alive(self):
        return self.health > 0

    def move_towards(self, target_position):
        direction = np.array(target_position) - self.position
        if np.linalg.norm(direction) > 0:
            step = direction / np.linalg.norm(direction)
            self.position += step.astype(int)


    def attack(self, target):
        if np.linalg.norm(self.position - target.position) <= self.range:
            target.health -= self.attack_power

class Map:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros(size)

    def is_within_bounds(self, position):
        return np.all(position >= 0) and np.all(position < self.size)

class RealTimeStrategySimulator:
    def __init__(self, map_size):
        self.map = Map(map_size)
        self.units = []
        self.time_step = 0

    def add_unit(self, unit):
        if self.map.is_within_bounds(unit.position):
            self.units.append(unit)

    def resolve_combat(self):
        for unit in self.units:
            if not unit.is_alive():
                continue

            enemies = [u for u in self.units if u.team != unit.team and u.is_alive()]
            if enemies:
                closest_enemy = min(enemies, key=lambda e: np.linalg.norm(unit.position - e.position))
                unit.attack(closest_enemy)

    def move_units(self):
        for unit in self.units:
            if not unit.is_alive():
                continue

            enemies = [u for u in self.units if u.team != unit.team and u.is_alive()]
            if enemies:
                closest_enemy = min(enemies, key=lambda e: np.linalg.norm(unit.position - e.position))
                unit.move_towards(closest_enemy.position)

    def update(self):
        self.move_units()
        self.resolve_combat()
        self.time_step += 1

    def display_state(self):
        print(f"Time Step: {self.time_step}")
        for unit in self.units:
            status = "Alive" if unit.is_alive() else "Dead"
            print(f"Unit {unit.id} (Team {unit.team}): Position {unit.position}, Health {unit.health}, Status {status}")

if __name__ == "__main__":
    # Initialize simulator
    simulator = RealTimeStrategySimulator(map_size=(20, 20))

    # Add units
    simulator.add_unit(Unit(id=1, team=1, position=(5, 5), health=100, attack_power=10, range=2))
    simulator.add_unit(Unit(id=2, team=2, position=(15, 15), health=100, attack_power=8, range=3))

    # Run simulation for 10 steps
    for _ in range(10):
        simulator.update()
        simulator.display_state()
        time.sleep(1)
