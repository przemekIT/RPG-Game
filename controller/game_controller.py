from tkinter import Tk
from view.game_view import GameView
from model.character import Player
from model.location import Village, Forest, Castle
from model.enemy import Goblin, Knight, Dragon
import random


class GameController:
    def __init__(self):
        self.root = Tk()
        self.root.title("RPG Text Game")
        self.player = Player(name="Bohater")
        self.view = GameView(self.root, self)

        # Lokacje
        self.locations = [Village(), Forest(), Castle()]
        self.current_location = random.choice(self.locations)
        self.enemy = None

        self.update_view()

    def update_view(self):
        self.view.display_location(self.current_location)
        self.view.update_stats(self.player)

    def run(self):
        self.root.mainloop()

    # === EKSPLORACJA ===
    def explore(self):
        self.view.show_message("Eksplorujesz teren...")
        # Szansa na spotkanie wroga
        encounter_chance = random.random()
        if encounter_chance < 0.6:  # 60% szansy na walkę
            self.enemy = random.choice([Goblin(), Knight(), Dragon()])
            self.start_battle()
        else:
            self.view.show_message("Nie znalazłeś żadnych wrogów.")
    
    def fight(self):
        """Rozpocznij losową walkę bez eksploracji."""
        self.enemy = random.choice([Goblin(), Knight(), Dragon()])
        self.start_battle()

    # === WALKA ===
    def start_battle(self):
        self.view.show_message(f"Rozpoczynasz walkę z {self.enemy.name}!")
        self.view.show_fight_interface(self.enemy)

    def player_attack(self):
        if not self.enemy:
            return

        player_damage = self.player.attack()
        self.enemy.hp -= player_damage
        self.view.show_message(f"Zadałeś {player_damage} obrażeń {self.enemy.name}.")

        if not self.enemy.is_alive():
            self.view.show_message(f"Pokonałeś {self.enemy.name}!")
            self.player.gain_exp(20)
            self.enemy = None
            self.update_view()
            self.view.restore_main_menu()
        else:
            self.enemy_attack()

    def enemy_attack(self):
        if not self.enemy:
            return

        enemy_damage = self.enemy.attack()
        self.player.hp -= enemy_damage
        self.view.show_message(f"{self.enemy.name} zadał Ci {enemy_damage} obrażeń.")

        if self.player.hp <= 0:
            self.view.show_message("Zginąłeś! Gra zakończona.")
            #self.view.disable_buttons()
            self.view.restore_main_menu()

    def attempt_escape(self):
        if not self.enemy:
            return

        chance = random.random()
        if chance < 0.5:
            self.view.show_message("Udało Ci się uciec!")
            self.enemy = None
            self.update_view()
        else:
            self.view.show_message("Nie udało się uciec! Wróg atakuje!")
            self.enemy_attack()

    # === LOKACJE ===
    def change_location(self):
        self.current_location = random.choice(self.locations)
        self.enemy = None
        self.update_view()

    # === EKWIPUNEK ===
    def open_inventory(self):
        self.view.show_inventory(self.player.inventory)

    def use_item(self, item):
        item.use(self.player)
        self.player.inventory.remove(item)
        self.view.show_message(f"Użyłeś {item.name}!")
        self.update_view()

    # === ROZMOWY ===
    def talk(self):
        if hasattr(self.current_location, "npc") and self.current_location.npc:
            self.view.show_npc_dialogue(self.current_location.npc)
        else:
            self.view.show_message("Nikogo tu nie ma do rozmowy.")