class Item:
    def __init__(self, name):
        self.name = name

    def use(self, player):
        pass


class HealthPotion(Item):
    def __init__(self):
        super().__init__("Mikstura zdrowia")
        self.heal_amount = 20

    def use(self, player):
        player.hp += self.heal_amount
        print(f"Używasz mikstury zdrowia. Przywrócono {self.heal_amount} HP.")
        return f"Używasz mikstury zdrowia. Przywrócono {self.heal_amount} HP."


class Sword(Item):
    def __init__(self):
        super().__init__("Miecz")
        self.attack_bonus = 5

    def use(self, player):
        player.attack_min += self.attack_bonus
        player.attack_max += self.attack_bonus
        print(f"Używasz miecza! Twoje obrażenia wzrosły o {self.attack_bonus}.")
        return f"Używasz miecza! Twoje obrażenia wzrosły o {self.attack_bonus}."


class Armor(Item):
    def __init__(self):
        super().__init__("Zbroja")
        self.defense_bonus = 10

    def use(self, player):
        player.hp += self.defense_bonus
        print(f"Używasz zbroi! Zwiększa to twoje HP o {self.defense_bonus}.")
        return f"Używasz zbroi! Zwiększa to twoje HP o {self.defense_bonus}."
