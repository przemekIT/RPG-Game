import random
from model.item import HealthPotion, Sword, Armor


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.exp = 0
        self.level = 1
        #self.inventory = []
        self.inventory = [HealthPotion(), Sword(), Armor()]

        self.attack_min = 5
        self.attack_max = 10

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.hp += 20
        print(f"Awansujesz na poziom {self.level}!")

    def attack(self):
        attack_damage = random.randint(self.attack_min, self.attack_max)
        print(f"Zadajesz {attack_damage} obrażeń.")
        return attack_damage

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Zdobytą przedmiot: {item.name}")

    def use_item(self, item):
        if item in self.inventory:
            item.use(self)
            self.inventory.remove(item)
