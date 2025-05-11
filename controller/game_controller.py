import tkinter as tk
from tkinter import Label, Button, Entry
import json
import random

from view.game_view import GameView
from model.character import Player
from model.location import Village, Forest, Castle
from model.enemy import Goblin, Knight, Dragon
from model.item import HealthPotion, Sword, Armor

ITEM_CLASSES = {"HealthPotion": HealthPotion, "Sword": Sword, "Armor": Armor}

LOCATION_CLASSES = {"Wioska": Village, "Las": Forest, "Zamek": Castle}


class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.player = None
        self.view = None
        self.locations = [Village(), Forest(), Castle()]
        self.current_location = random.choice(self.locations)
        self.enemy = None

    def start_new_game(self):
        self.view.prompt_player_name(self._initialize_game_with_name)

    def _initialize_game_with_name(self, player_name):
        self.player = Player(player_name)
        self.root.deiconify()
        self.update_view()
        self.view.show_message(f"Nowa gra rozpoczęta dla: {self.player.name}")

    def save_game(self, filename="C:/Users/maria/RPG-Game/savegame.json"):
        print("Zapisuję grę...")
        data = {
            "location": self.current_location.name,
            "player": {
                "name": self.player.name,
                "hp": self.player.hp,
                "level": self.player.level,
                "exp": self.player.exp,
                "inventory": [
                    item.__class__.__name__ for item in self.player.inventory
                ],
            },
        }

        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
                self.view.show_message("Gra została zapisana.")
        except Exception as e:
            print(f"Błąd przy zapisie gry: {e}")
            self.view.show_message(f"Błąd przy zapisie gry: {e}")

    def load_game(self, filename="C:/Users/maria/RPG-Game/savegame.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            location_name = data["location"]
            self.current_location = LOCATION_CLASSES[location_name]()

            self.player = Player(data["player"]["name"])
            self.player.hp = data["player"]["hp"]
            self.player.level = data["player"]["level"]
            self.player.exp = data["player"]["exp"]
            self.player.inventory = [
                ITEM_CLASSES[name]() for name in data["player"]["inventory"]
            ]

            if not self.view:
                self.view = GameView(self.root, self)

            self.root.deiconify()

            self.view.display_location(self.current_location)
            self.view.update_stats(self.player)
            self.view.show_message("Gra została wczytana.")

        except Exception as e:
            if self.view:
                self.view.show_message(f"Błąd wczytywania gry: {str(e)}")
            else:
                print(f"Błąd wczytywania gry: {str(e)}")

    def update_view(self):
        self.view.display_location(self.current_location)
        self.view.update_stats(self.player)

    def run(self):
        self.view = GameView(self.root, self)
        self.view.show_start_screen(self.on_new_game, self.on_load_game)
        self.root.mainloop()

    def explore(self):
        self.view.show_message("Eksplorujesz teren...")
        encounter_chance = random.random()
        if encounter_chance < 0.3:
            self.enemy = random.choice([Goblin(), Knight(), Dragon()])
            self.start_battle()
        else:
            self.view.show_message("Nie znalazłeś żadnych wrogów... Eksploruj dalej")

    def fight(self):
        self.enemy = random.choice([Goblin(), Knight(), Dragon()])
        self.start_battle()

    def start_battle(self):
        self.view.show_message(f"Rozpoczynasz walkę z {self.enemy.name}!")
        self.view.show_fight_interface(self.enemy)

    def player_attack(self):
        if not self.enemy:
            return

        player_damage = self.player.attack()
        self.enemy.hp -= player_damage
        self.view.show_message(f"Zadałeś {player_damage} obrażeń {self.enemy.name}.")
        self.view.update_enemy_hp(self.enemy)
        self.view.update_stats(self.player)

        if not self.enemy.is_alive():
            self.view.show_message(
                f"Pokonałeś {self.enemy.name}! Dostajesz 50 punktów HP i 20 EXP. Awansujesz na kolejny poziom!"
            )
            self.player.hp += 50
            self.player.gain_exp(20)
            reward = random.choice([HealthPotion(), Sword(), Armor(), None])
            if reward:
                self.player.inventory.append(reward)
                self.view.show_message(f"Znalazłeś przedmiot: {reward.name}!")
            self.enemy = None
            self.update_view()
            self.view.show_main_menu()
        else:
            self.enemy_attack()

    def enemy_attack(self):
        if not self.enemy:
            return

        enemy_damage = self.enemy.attack()
        self.player.hp -= enemy_damage
        self.view.show_message(f"{self.enemy.name} zadał Ci {enemy_damage} obrażeń.")
        self.view.update_stats(self.player)

        if self.player.hp <= 0:
            self.view.show_message("Zginąłeś! Gra zakończona.")
            self.view.show_game_over_screen()
        else:
            self.view.show_message("Kontynuuj atak lub spróbuj uciec")

    def attempt_escape(self):
        if not self.enemy:
            return

        if random.random() < 0.5:
            self.view.show_message("Udało Ci się uciec!")
            self.enemy = None
            self.update_view()
            self.view.show_main_menu()
        else:
            self.view.show_message("Nie udało się uciec! Wróg atakuje!")
            self.enemy_attack()

    def change_location(self):
        self.current_location = random.choice(self.locations)
        self.enemy = None
        self.update_view()

    def open_inventory(self):
        self.view.show_inventory(self.player.inventory)

    def use_item(self, item):
        item.use(self.player)
        self.player.inventory.remove(item)
        self.view.show_message(f"Użyłeś {item.name}!")

        if item.name == "Mikstura zdrowia":
            self.view.show_message(f"Przywrócono {item.heal_amount} HP.")
        elif item.name == "Miecz":
            self.view.show_message(f"Twoje obrażenia wzrosły o {item.attack_bonus}")
        elif item.name == "Zbroja":
            self.view.show_message(f"Zbroja zwiększa twoje HP o {item.defense_bonus}")

        self.view.update_stats(self.player)

    def talk(self):
        if hasattr(self.current_location, "npc") and self.current_location.npc:
            self.view.show_npc_dialogue(self.current_location.npc)
        else:
            self.view.show_message("Nikogo tu nie ma do rozmowy.")

    # def talk_to_npc(self, npc):
    #     self.view.show_message(f"{npc.name}: {npc.talk}")
    #     if random.random() < 0.5:
    #         gift = random.choice([HealthPotion(), Sword(), Armor(), None])
    #         if gift:
    #             self.player.inventory.append(gift)
    #             self.view.show_message(f"{npc.name} dał Ci przedmiot: {gift.name}!")

    def restart_game(self):
        self.root.destroy()
        new_game = GameController()
        new_game.run()

    def on_new_game(self):
        self.view.prompt_player_name(self._initialize_game_with_name)

    def on_load_game(self):
        self.load_game()
