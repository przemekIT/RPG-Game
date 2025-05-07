import json
from model.player import Player
from model.enemy import Enemy
from model.GameNpc import GameNpc
from model.objects import GameObjects
import random
from typing import List

class GameCharacter:
    def __init__(self, data, data_items):
        self.data = data
        self.data_items = data_items

    def create_player(self, name, class_name) -> List[Player]:
        character_data = self.data.get(class_name)
        if character_data:
            return Player(
                name,
                character_data['name'], 
                character_data['hp'], 
                0,
                character_data['attack'], 
                character_data['defense'])
        else:
            raise ValueError(f"Character '{self.type}' not found in the data.")
    
    def get_player(self) -> Player:
        return self.player
    
    def create_enemy(self) -> List[Enemy]: 
        enemies_data = self.data["Enemies"]
        self.enemies = []

        for enemy, enemy_data in enemies_data.items():
            enemy = Enemy(
                enemy_data['name'],
                enemy_data['hp'],
                enemy_data['attack'],
                enemy_data['defense'],
                enemy_data['exp'],
                enemy_data['description']
            )
            self.enemies.append(enemy)

        return self.enemies
    
    def get_random_enemy(self) -> Enemy:
        template_enemy = random.choice(self.enemies)
        return template_enemy.clone()


    def create_nps(self) -> List[GameNpc]:
        npcs_data = self.data["NPCs"]
        self.npcs = []

        for npc, npc_data in npcs_data.items():
            npc = GameNpc(
                npc_data["name"],
                npc_data["role"],
                npc_data["description"],
                npc_data["services"],
                npc_data["location"],
                npc_data["dialogue"]
            )
            self.npcs.append(npc)

        return self.npcs

    def get_random_nps(self) ->GameNpc:
        template_nps = random.choice(self.npcs)
        return template_nps.clone()
    
    def set_objects(self) ->List[GameObjects]:
        self.items = []

        for category in ['weapons', 'armors', 'consumables']:
            for item_data in self.data.get(category, []):
                item = GameObjects(
                    item_data["name"],
                    item_data["type"],
                    item_data["description"],
                    item_data["stats"]
                    
                )
                self.items.append(item)

        return self.items

    def get_object(self) ->GameObjects:
        return self.items

   