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

    def special_attack(self, player):
        # Domyślnie brak specjalnego ataku
        return None


class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Smok", hp=100, attack_min=10, attack_max=20)

    def special_attack(self, player):
        damage = 15
        player.hp -= damage
        return f"Smok zionie ogniem i zadaje {damage} obrażeń!"


class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", hp=80, attack_min=5, attack_max=10)

    def special_attack(self, player):
        stolen_hp = 10
        player.hp -= stolen_hp
        self.hp += stolen_hp
        return f"Goblin podstępnie kradnie Ci {stolen_hp} HP i leczy siebie!"


class Knight(Enemy):
    def __init__(self):
        super().__init__(name="Rycerz", hp=110, attack_min=8, attack_max=25)

    def special_attack(self, player):
        damage = random.randint(20, 25)
        player.hp -= damage
        return f"Rycerz wykonuje miażdżący cios i zadaje {damage} obrażeń!"
