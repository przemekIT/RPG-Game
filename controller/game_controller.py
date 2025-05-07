import tkinter as tk
from tkinter import Label, Button, Entry
from view.game_view import GameView
from model.character import Player
from model.location import Village, Forest, Castle
from model.enemy import Goblin, Knight, Dragon
import random
from model.character import Player, save_player, load_player


class GameController:
    def __init__(self):
        self.root = tk.Tk()  # Główne okno aplikacji
        self.root.title("RPG Text Game")
        self.player = Player(name="Bohater")  
        self.view = GameView(self.root, self)

        # Lokacje
        self.locations = [Village(), Forest(), Castle()]
        self.current_location = random.choice(self.locations)
        self.enemy = None

        self.update_view()

    def show_start_screen(self):
        """Okno startowe"""
        start_window = tk.Toplevel(self.root)
        start_window.title("Witaj w RPG game!")
        start_window.geometry("300x200")
        start_window.resizable(False, False)

        label = Label(start_window, text="Wybierz opcję:", font=("Arial", 12, "bold"))
        label.pack(pady=20)

        # Przycisk 'Nowa Gra'
        new_game_btn = Button(start_window, text="Nowa Gra", width=20,
                              command=lambda: [start_window.destroy(), self.ask_player_name()])
        new_game_btn.pack(pady=5)


        # Przycisk 'Wczytaj Grę'
        load_game_btn = Button(start_window, text="Wczytaj Grę", width=20,
                               command=lambda: [start_window.destroy(), self.load_game()])
        load_game_btn.pack(pady=5)

    def ask_player_name(self):
        """Pole do wpisania imienia bohatera."""
        name_window = tk.Toplevel(self.root)
        name_window.title("Wprowadź Imię Bohatera")
        name_window.geometry("300x150")

        label = Label(name_window, text="Podaj imię bohatera:", font=("Arial", 12))
        label.pack(pady=20)

        self.name_entry = Entry(name_window, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        start_btn = Button(name_window, text="Start", width=20, 
                           command=lambda: [self.start_new_game(name_window)])
        start_btn.pack(pady=5)

    def start_new_game(self, name_window):
        """Po kliknięciu przycisku Start, rozpoczynamy nową grę z imieniem bohatera."""
        player_name = self.name_entry.get()
        self.player = Player(player_name)
        save_player(self.player)
        self.update_view()

        # Zamykanie okna do wpisania imienia
        name_window.destroy()

        # Po zamknięciu okna z imieniem, uruchamiamy główną pętlę gry
        self.view.show_message(f"Nowa gra rozpoczęta dla: {self.player.name}")

        # Uruchomienie głównej pętli gry
        self.run()

    def load_game(self):
        """Funkcja do wczytania zapisanej gry."""
        try:
            self.player = load_player()
            self.update_view()
            self.view.show_message(f"Wczytano gracza: {self.player.name}, poziom {self.player.level}")
        except FileNotFoundError:
            self.view.show_message("Nie znaleziono zapisu gry. Tworzenie nowej postaci...")
            self.new_game()

    def update_view(self):
        """Aktualizuje widok gry."""
        self.view.display_location(self.current_location)
        self.view.update_stats(self.player)

    def run(self):
        """Uruchamienie głównej pętly gry"""
        self.root.mainloop()

    # === EKSPLORACJA ===
    def explore(self):
        self.view.show_message("Eksplorujesz teren...")
        encounter_chance = random.random()
        if encounter_chance < 0.6:
            self.enemy = random.choice([Goblin(), Knight(), Dragon()])
            self.start_battle()
        else:
            self.view.show_message("Nie znalazłeś żadnych wrogów.")

    def fight(self):
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
            self.view.restore_main_menu()

    def attempt_escape(self):
        if not self.enemy:
            return

        chance = random.random()
        if chance < 0.5:
            self.view.show_message("Udało Ci się uciec!")
            self.enemy = None
            self.update_view()
            self.view.restore_main_menu()
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
        self.update_view()

    def talk(self):
        if hasattr(self.current_location, "npc") and self.current_location.npc:
            self.view.show_npc_dialogue(self.current_location.npc)
        else:
            self.view.show_message("Nikogo tu nie ma do rozmowy.")