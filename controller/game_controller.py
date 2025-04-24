from tkinter import Tk
from view.game_view import GameView
from model.character import Player
from model.location import Village, Forest, Castle
from model.enemy import Goblin, Knight, Dragon
from tkinter import messagebox
import random


class GameController:
    def __init__(self):
        self.root = Tk()  # Tworzymy główne okno Tkintera
        self.root.title("RPG Text Game")
        self.player = Player(name="Bohater")
        self.view = GameView(
            self.root, self
        )  # Tworzymy widok i przekazujemy do niego główne okno Tkintera

        # Lokacje
        # self.locations = {"forest": Forest(), "castle": Castle(), "village": Village()}
        # self.current_location = self.locations["village"]
        self.locations = [Village(), Forest(), Castle()]
        self.current_location = random.choice(self.locations)
        self.update_view()

        self.enemy = None

    def update_view(self):
        self.view.display_location(self.current_location)
        self.view.update_stats(self.player)

    def explore(self):
        if self.current_location.name == "Las":
            self.enemy = Goblin()
        elif self.current_location.name == "Zamek":
            self.enemy = Knight()
        elif self.current_location.name == "Wioska":
            self.enemy = Dragon()

        self.start_battle()

    def start_battle(self):
        while self.enemy.is_alive() and self.player.hp > 0:
            # Ruch gracza
            self.view.show_message("Twoja kolej! Atakuj!")
            player_attack = self.player.attack()
            self.enemy.hp -= player_attack
            self.view.show_message(
                f"Zadałeś {player_attack} obrażeń {self.enemy.name}."
            )

            if not self.enemy.is_alive():
                self.view.show_message(f"Pokonałeś {self.enemy.name}!")
                self.player.gain_exp(20)
                break

            # Ruch przeciwnika
            enemy_attack = self.enemy.attack()
            self.player.hp -= enemy_attack
            self.view.show_message(
                f"{self.enemy.name} atakuje! Zadał {enemy_attack} obrażeń."
            )

            if self.player.hp <= 0:
                self.view.show_message("Zginąłeś! Gra zakończona.")
                break

        self.update_view()

    def run(self):
        """Uruchomienie gry. Metoda ta wywołuje mainloop() na głównym oknie Tkintera."""
        self.root.mainloop()  # Uruchomienie głównej pętli Tkintera dla GUI

    def open_inventory(self):
        self.view.show_message("Otwierasz ekwipunek...")
        inventory_list = "\n".join(
            [f"{i+1}. {item.name}" for i, item in enumerate(self.player.inventory)]
        )
        if not inventory_list:
            self.view.show_message("Ekwipunek jest pusty.")
        else:
            self.view.show_message(f"Twoj ekwipunek to:\n{inventory_list}")

    def talk(self):
        self.view.show_message("Rozpoczynasz rozmowę...")
        if hasattr(self.current_location, "npc"):
            self.view.show_message(self.current_location.npc.talk())
        else:
            self.view.show_message("Nikogo tu nie ma do rozmowy.")

    def fight(self):
        self.enemy = Goblin()
        self.view.show_message(f"Rozpoczynasz walke z {self.enemy.name}!")
        self.view.show_fight_interface(self.enemy)

    def change_location(self):
        self.current_location = random.choice(self.locations)
        self.view.display_location(self.current_location)
