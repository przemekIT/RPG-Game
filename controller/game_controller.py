import tkinter as tk
from tkinter import Label, Button, Entry
from view.game_view import GameView
from model.character import Player
from model.location import Village, Forest, Castle
from model.enemy import Goblin, Knight, Dragon
import random
from model.character import Player, save_player, load_player
from model.item import HealthPotion, Sword, Armor


class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Ukryj główne okno do czasu startu gry
        self.player = None
        self.view = None
        self.locations = [Village(), Forest(), Castle()]
        self.current_location = random.choice(self.locations)
        self.enemy = None

    def show_start_screen(self):
        """Okno startowe"""
        start_window = tk.Toplevel(self.root)
        start_window.title("Witaj w RPG game!")
        start_window.geometry("300x200")
        start_window.resizable(False, False)

        label = Label(start_window, text="Wybierz opcję:", font=("Arial", 12, "bold"))
        label.pack(pady=20)

        # Przycisk 'Nowa Gra'
        new_game_btn = Button(
            start_window,
            text="Nowa Gra",
            width=20,
            command=lambda: [start_window.destroy(), self.ask_player_name()],
        )
        new_game_btn.pack(pady=5)

        # Przycisk 'Wczytaj Grę'
        load_game_btn = Button(
            start_window,
            text="Wczytaj Grę",
            width=20,
            command=lambda: [start_window.destroy(), self.load_game()],
        )
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

        start_btn = Button(
            name_window,
            text="Start",
            width=20,
            command=lambda: [self.start_new_game(name_window)],
        )
        start_btn.pack(pady=5)

    def start_new_game(self, name_window):
        player_name = self.name_entry.get()
        self.player = Player(player_name)
        save_player(self.player)

        name_window.destroy()

        self.root.deiconify()  # Pokaż główne okno
        self.view = GameView(self.root, self)
        self.update_view()
        self.view.show_message(f"Nowa gra rozpoczęta dla: {self.player.name}")

        self.run()

    def load_game(self):
        """Funkcja do wczytania zapisanej gry."""
        try:
            self.player = load_player()
            self.update_view()
            self.view.show_message(
                f"Wczytano gracza: {self.player.name}, poziom {self.player.level}"
            )
        except FileNotFoundError:
            self.view.show_message(
                "Nie znaleziono zapisu gry. Tworzenie nowej postaci..."
            )
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
        if encounter_chance < 0.3:
            self.enemy = random.choice([Goblin(), Knight(), Dragon()])
            self.start_battle()
        else:
            self.view.show_message("Nie znalazłeś żadnych wrogów... Eksploruj dalej")

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
        self.view.update_enemy_hp(self.enemy)
        # self.update_view()
        self.view.update_stats(self.player)

        if not self.enemy.is_alive():
            self.view.show_message(
                f"Pokonałeś {self.enemy.name}! Dostajesz 70 punktow hp i 20 exp. Awansujesz na kolejny poziom!"
            )
            self.player.hp += 70
            self.player.gain_exp(20)
            reward = random.choice([HealthPotion(), Sword(), Armor(), None])
            if reward:
                self.player.inventory.append(reward)
                self.view.show_message(f"Znalazłeś przedmiot: {reward.name}!")
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
        self.view.update_stats(self.player)
        if self.player.hp <= 0:
            # self.view.show_message("Zginąłeś! Gra zakończona. Gra rozpocznie się od nowa za 5 sekund.")
            # self.root.after(5000, self.restart_game)  # 5000 ms = 5 sekund
            self.view.show_message("Zginąłeś! Gra zakończona.")
            self.view.show_game_over_screen()
        else:
            self.view.show_message("Kontynuuj atak lub spróbuj uciec")
            self.view.update_stats(self.enemy)
        # self.view.update_enemy_hp(self.enemy)
        # self.update_view()

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
        if item.name == "Mikstura zdrowia":
            self.view.show_message(f"Przywrócono {item.heal_amount} HP.")
        elif item.name == "Miecz":
            self.view.show_message(f"Twoje obrażenia wzrosły o {item.attack_bonus}")
        elif item.name == "Zbroja":
            self.view.show_message(
                f"Używasz zbroi! Zwiększa to twoje HP o {item.defense_bonus}"
            )
        self.view.update_stats(self.player)
        if self.enemy:
            self.view.update_enemy_hp(self.enemy)

    def talk(self):
        if hasattr(self.current_location, "npc") and self.current_location.npc:
            self.view.show_npc_dialogue(self.current_location.npc)
        else:
            self.view.show_message("Nikogo tu nie ma do rozmowy.")

    def talk_to_npc(self, npc):
        self.view.show_message(f"{npc.name}: {npc.talk}")

        # NPC może dać przedmiot
        if random.random() < 0.5:  # 50% szansy
            gift = random.choice([HealthPotion(), Sword(), Armor(), None])
            self.player.inventory.append(gift)
            self.view.show_message(f"{npc.name} dał Ci przedmiot: {gift.name}!")

    def restart_game(self):
        self.root.destroy()  # Zamknij aktualne okno gry
        new_game = GameController()  # Utwórz nową instancję kontrolera
        new_game.show_start_screen()
        new_game.run()
