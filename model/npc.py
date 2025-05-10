import random
from model.item import HealthPotion, Sword, Armor


class NPC:
    def __init__(self, name, dialogues, can_give_items=False):
        self.name = name
        self.dialogues = dialogues  # lista krotek: (pytanie_gracza, odpowiedz_npc)
        self.can_give_items = can_give_items

    def get_dialogue_options(self):
        return [q for q, _ in self.dialogues]

    def respond_to(self, question):
        for q, a in self.dialogues:
            if q == question:
                return f"{self.name} mówi: {a}"
        return f"{self.name} nie wie, co powiedzieć..."

    def give_item(self):
        if self.can_give_items and random.random() < 0.3:  # 30% szansy
            return random.choice([HealthPotion(), Sword(), Armor()])
        return None
