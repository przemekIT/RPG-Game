from model.player import Player
from model.enemy import Enemy
from model.GameNpc import GameNpc
from model.objects import GameObjects
import random
from typing import Dict, List

class GameCharacter:
    def __init__(self, data: Dict[str, Dict], data_items: Dict[str, List[Dict]]) -> None:
        self.data: Dict[str, Dict] = data
        self.data_items: Dict[str, List[Dict]] = data_items

    def create_player(self, name, class_name) -> Player:
        character_data = self.data.get(class_name)
        if character_data:
            self.player = Player(
                name,
                character_data['name'], 
                character_data['hp'], 
                0,
                character_data['attack'], 
                character_data['defense'])
            return self.player
        else:
            raise ValueError(f"Character '{class_name}' not found in the data.")
    
    def get_player(self) -> Player:
        return self.player
    
    def load_player(self, data: dict):
        player = Player(
            name=data.get("name", ""),
            class_name=data.get("class_name", ""),
            hp=data.get("hp", 100),
            sp=data.get("sp", 0),
            attack=data.get("attack", 10),
            defense=data.get("defence", 5)
        )

        player.gold = data.get("gold", 0)

        inventory_data = data.get("inventory", [])
        for item_dict in inventory_data:
            item = GameObjects(
                name=item_dict["name"],
                type_=item_dict["type"],
                description=item_dict["description"],
                stat=item_dict["stat"]
            )
            player.add_item(item)

        return player
    
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
            for item_data in self.data_items.get(category, []):
                item = GameObjects(
                    item_data["name"],
                    item_data["type"],
                    item_data["description"],
                    item_data["stat"]
                    
                )
                self.items.append(item)

        return self.items

    def get_object(self) ->GameObjects:
        return self.items
    
    

   