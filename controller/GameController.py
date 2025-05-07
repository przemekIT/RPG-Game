import tkinter as tk
from view.GameGUI import GameGUI
from view.CreateGame import CreateGame
from view.GameScreen import GameScreen
from view.InventoryGUI import InventoryGUI
from model.GameCharacter import GameCharacter
from model.player import Player
from model.enemy import Enemy
from model.objects import GameObjects
import json
from pathlib import Path
import random
import threading
import time
from typing import List, Optional

class GameController:
    ESCAPE_CHANCE = 0.3
    ENEMY_HIT_CHANCE = 0.5

    def __init__(self):
        self.root = tk.Tk()
        self.data_player = self.load_data("assets/characters.json")
        self.dataGUI = self.load_data("assets/mainGUI.json")
        self.data_items = self.load_data("assets/items.json")
        # self.inventory = InventoryGUI(self.root, self.data_items)
        
        self.gui = GameGUI(self.root, self.dataGUI, self)
        self.characters = GameCharacter(self.data_player, self.data_items)
        self.current_zon = None
        self.zone_steps = 0

    def load_data(self, file) -> dict:
        basePath = Path(__file__).parent
        file_path = (basePath / ".." / file ).resolve()
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def new_game(self):
        self.gui.clear_screen()
        self.new_create = CreateGame(self.gui.main_frame, self)

    def create_character(self, name, char_class):
        self.player = self.characters.create_player(name, char_class)
        self.enemys = self.characters.create_enemy()
        self.npcs = self.characters.create_nps()
        self.start_game()

    def start_game(self):
        self.gui.clear_screen()
        self.game_screen = GameScreen(self.root, self, self.dataGUI)
        self.update_player_info()

    def update_player_info(self):
        self.game_screen.clear_frame(self.game_screen.right_frame)
        self.game_screen.player_info(self.player)

    def update_enemy_info(self):
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.enemy_info(self.enemy)

    def go_to_castle(self):
        # self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        # self.game_screen.clear_frame(self.game_screen.left_frame)
        self.current_zon = self.go_to_castle

        self.wait_and_continue()

    def go_to_forest(self):
        pass

    def go_to_gate(self):
        pass

    def random_event(self) -> str:
        events = ["battle", "peaceful"]
        return random.choice(events)

    def return_to_main_actions(self):
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.clear_frame(self.game_screen.left_frame)
        self.game_screen.create_start_action_buttons()
        self.game_screen.update_event_log("--- Returned to main actions ---")

    def attack_action(self):
        player_attack = self.player.get_attack()
        enemy_defense = self.enemy.get_defense()
        damage_to_enemy = max(player_attack - enemy_defense, 0)
        self.enemy.update_stat("hp", damage_to_enemy)

        self.update_enemy_info()
        self.game_screen.update_event_log(f"{self.enemy.name} - {damage_to_enemy} damage")

        if self.enemy.hp <= 0:
            self.game_screen.update_event_log(f"{self.enemy.name} - is Die")
            return self.go_to_castle()

        if random.random() < GameController.ENEMY_HIT_CHANCE:
            damage_to_player = max(self.enemy.get_attack() - self.player.get_defense(), 0)
            self.player.update_stat("hp", damage_to_player)

            self.update_player_info()
            self.game_screen.update_event_log(f"{self.player.name} - {damage_to_player} damage")

            if self.player.hp <= 0:
                self.game_screen.update_event_log("You die!")
        self.zone_steps += 1

    def defend_action(self):
        if random.random() < GameController.ENEMY_HIT_CHANCE:
            damage_to_player = max(self.enemy.get_attack() - self.player.get_defense(), 0)
            self.player.update_stat("hp", damage_to_player)
            self.game_screen.update_event_log(f"You defend! {self.enemy.name} deals {damage_to_player} damage")

        else:
            self.game_screen.update_event_log(f"{self.enemy.name} missed the attack!")

        self.update_player_info()

        if self.player.hp <= 0:
            self.game_screen.update_event_log("You die!")

        self.zone_steps += 1

    def run_action(self):
        if random.random() < GameController.ESCAPE_CHANCE:
            self.game_screen.update_event_log(f"{self.player.name} successfully fled from the battle!")
            return self.current_zon()

        self.game_screen.update_event_log(f"{self.player.name} failed to escape!")

        if random.random() < GameController.ENEMY_HIT_CHANCE:
            damage_to_player = max(self.enemy.get_attack() - self.player.get_defense(), 0)
            self.player.update_stat("hp", damage_to_player)
            self.update_player_info()
            self.game_screen.update_event_log(f"{self.player.name} receives {damage_to_player} damage!")

            if self.player.hp <= 0:
                self.game_screen.update_event_log("You die!")

        self.zone_steps += 1

    def wait_and_continue(self):
        self.game_screen.clear_frame(self.game_screen.center_buttons_frame)
        self.game_screen.clear_frame(self.game_screen.left_frame)

        self.stop_waiting = False

        def return_home():
            self.stop_waiting = True
            self.return_to_main_actions() 

        can_return = self.zone_steps >= 15

        self.game_screen.create_return_home_button(
            command=return_home,
            enabled=can_return
        )  

        def delayed_event():
            time.sleep(3)
            if not self.stop_waiting:
                self.root.after(0, self.zone_event)

        threading.Thread(target=delayed_event, daemon=True).start()

    def zone_event(self):
        event = self.random_event()

        if event == "battle":
            self.enemy = self.characters.get_random_enemy()
            self.update_enemy_info()
            self.game_screen.create_battle_action_buttons()

        elif event == "peaceful":
            self.npc = self.characters.get_random_nps()
            self.game_screen.npc_info(self.npc)
            self.game_screen.create_npc_action_buttons(self.npc)
            self.zone_steps += 1

    def npc_action(self, npc, service):
        npc_services = {
            "Upgrade Weapons": lambda: self.game_screen.update_event_log(f"{npc.name} upgrades your weapons!"),
            "Upgrade Armor": lambda: self.game_screen.update_event_log(f"{npc.name} upgrades your armor!"),
            "Heal": lambda: self.game_screen.update_event_log(f"{npc.name} healed you to full HP!"),
            "Buy Potions": lambda: self.game_screen.update_event_log(f"You bought potions from {npc.name}!"),
            "Buy Items": lambda: self.game_screen.update_event_log(f"You bought items from {npc.name}!"),
            "Sell Items": lambda: self.game_screen.update_event_log(f"You sold items to {npc.name}!"),
            "Give Information": lambda: self.game_screen.update_event_log(f"{npc.name} shares valuable information with you."),
            "Offer Side Quest": lambda: self.game_screen.update_event_log(f"{npc.name} offers you a side quest!"),
        }

        action = npc_services.get(service)
        if action:
            action()
        else:
            self.game_screen.update_event_log("Unknown service")
            print("Unknown service")

    def run(self):
        self.root.mainloop()