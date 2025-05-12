import random


class Enemy:
    def __init__(self, name, base_hp, base_min, base_max, player_level=1):
        self.name = name
        self.hp = base_hp + player_level * 5
        # self.attack_min = base_min + player_level
        # self.attack_max = base_max + player_level * 2
        self.attack_min = base_min + (player_level - 1) * 2
        self.attack_max = base_max + (player_level - 1) * 2
        self.hp = base_hp + (player_level - 1) * 20

    def attack(self):
        return random.randint(self.attack_min, self.attack_max)

    def is_alive(self):
        return self.hp > 0

    def special_attack(self, player):
        return None


class Dragon(Enemy):
    def __init__(self, player_level=1):
        super().__init__(
            name="Smok",
            base_hp=100,
            base_min=10,
            base_max=20,
            player_level=player_level,
        )

    def special_attack(self, player):
        damage = 15 + player.level
        player.hp -= damage
        return f"Smok zionie ogniem i zadaje {damage} obrażeń!"


class Goblin(Enemy):
    def __init__(self, player_level=1):
        super().__init__(
            name="Goblin",
            base_hp=80,
            base_min=5,
            base_max=10,
            player_level=player_level,
        )

    def special_attack(self, player):
        stolen_hp = 10
        player.hp -= stolen_hp
        self.hp += stolen_hp
        return f"Goblin podstępnie kradnie Ci {stolen_hp} HP i leczy siebie!"


class Knight(Enemy):
    def __init__(self, player_level=1):
        super().__init__(
            name="Rycerz",
            base_hp=110,
            base_min=8,
            base_max=25,
            player_level=player_level,
        )

    def special_attack(self, player):
        damage = random.randint(20, 25)
        player.hp -= damage
        return f"Rycerz wykonuje miażdżący cios i zadaje {damage} obrażeń!"
