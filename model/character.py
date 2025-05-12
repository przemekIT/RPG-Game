import random
from model.item import HealthPotion, Sword, Armor
import json

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.exp = 0
        self.level = 1
        self.inventory = [HealthPotion(), Sword(), Armor()]

        self.attack_min = 5
        self.attack_max = 20

    item_classes = {"Health Potion": HealthPotion, "Sword": Sword, "Armor": Armor}

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "exp": self.exp,
            "level": self.level,
            "inventory": [item.name for item in self.inventory],
        }

    @staticmethod
    def from_dict(data):
        name = data["name"]
        hp = data.get("hp", 100)
        exp = data.get("exp", 0)
        level = data.get("level", 1)
        inventory_names = data.get("inventory", [])
        inventory = [
            item_classes[name]() for name in inventory_names if name in item_classes
        ]
        return Player(name, hp, exp, level, inventory)

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.attack_min += 1
        self.attack_max += 2
        # self.hp += 20
        print(f"Awansujesz na poziom {self.level}! Zyskałeś więcej HP i siły!")

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

# def save_player(player, filename="save.json"):
#     with open(filename, "w") as f:
#         json.dump(player.to_dict(), f)


# def load_player(filename="save.json"):
#     with open(filename, "r") as f:
#         data = json.load(f)
#         # return Player.from_dict(data)
#         player = Player(name)
#         player.hp = hp
#         player.exp = exp
#         player.level = level
#         player.inventory = inventory
#         return player
