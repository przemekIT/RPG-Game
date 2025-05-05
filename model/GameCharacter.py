import json
from model.player import Player
from model.enemy import Enemy

class GameCharacter:
    def __init__(self, data):
        self.data = data
        # self.player = self.create_player()

    def create_player(self, name, class_name):
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
    
    def get_player(self):
        return self.player
    
    def create_enemy(self):
        enemies_data = self.data["Enemies"]
        enemies = []

        for enemy, enemy_data in enemies_data.items():
            enemy = Enemy(
                enemy_data['name'],
                enemy_data['hp'],
                enemy_data['attack'],
                enemy_data['defense'],
                enemy_data['exp'],
                enemy_data['description']
            )
            enemies.append(enemy)

        return enemies


    def nps(self):
        pass

   