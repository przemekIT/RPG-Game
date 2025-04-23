import random


class Enemy:
    def __init__(self, name, hp, attack_min, attack_max):
        self.name = name
        self.hp = hp
        self.attack_min = attack_min
        self.attack_max = attack_max

    def attack(self):
        return random.randint(self.attack_min, self.attack_max)

    def is_alive(self):
        return self.hp > 0


class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", hp=30, attack_min=5, attack_max=10)


class Knight(Enemy):
    def __init__(self):
        super().__init__(name="Rycerz", hp=50, attack_min=8, attack_max=15)


class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Smok", hp=100, attack_min=15, attack_max=25)
