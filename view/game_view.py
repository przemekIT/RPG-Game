import tkinter as tk
from tkinter import Frame, Label, Button, Text, Scrollbar, END, LEFT, RIGHT, BOTH, Y

class GameView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Gra RPG")  # Dodaj tytuł okna
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # === Panel Statystyk ===
        self.stats_frame = Frame(self.root)
        self.stats_frame.pack(fill="x", pady=5)

        self.stats_label = Label(self.stats_frame, text="Statystyki gracza", anchor="w", justify="left", font=("Arial", 10))
        self.stats_label.pack(side=LEFT, padx=10)

        # === Panel Lokacji ===
        self.location_frame = Frame(self.root)
        self.location_frame.pack(fill="x", pady=5)

        self.location_label = Label(self.location_frame, text="Lokalizacja: ???", font=("Arial", 12, "bold"))
        self.location_label.pack()

        # === Log Gry ===
        self.log_frame = Frame(self.root)
        self.log_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.log_text = Text(self.log_frame, wrap="word", height=15, state="disabled", bg="#f0f0f0")
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        # === Panel Akcji (Przyciski) ===
        self.action_frame = Frame(self.root)
        self.action_frame.pack(pady=10)

        self.explore_button = Button(self.action_frame, text="Eksploruj", width=15, command=self.controller.explore)
        self.explore_button.pack(side=LEFT, padx=5)

        self.inventory_button = Button(self.action_frame, text="Ekwipunek", width=15, command=self.controller.open_inventory)
        self.inventory_button.pack(side=LEFT, padx=5)

        self.talk_button = Button(self.action_frame, text="Rozmowa", width=15, command=self.controller.talk)
        self.talk_button.pack(side=LEFT, padx=5)

        self.fight_button = Button(self.action_frame, text="Walka", width=15, command=self.controller.fight)
        self.fight_button.pack(side=LEFT, padx=5)

        self.change_location_button = Button(self.action_frame, text="Zmień Lokację", width=15, command=self.controller.change_location)
        self.change_location_button.pack(side=LEFT, padx=5)

        # === Panel Walki (Ukryty na start) ===
        self.battle_frame = Frame(self.root)

    # --- Funkcje GUI ---

    def display_location(self, location):
        self.location_label.config(text=f"Lokalizacja: {location.name}")
        self.log(f"Jesteś w {location.name}. {location.description}")

    def update_stats(self, player):
        self.stats_label.config(
            text=f"{player.name} | HP: {player.hp} | EXP: {player.exp} | Poziom: {player.level}"
        )

    def show_message(self, message):
        self.log(message)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)
        self.log_text.config(state="disabled")

    def clear_action_buttons(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

    def clear_battle_frame(self):
        for widget in self.battle_frame.winfo_children():
            widget.destroy()
        #self.battle_frame.pack_forget()

    def show_fight_interface(self, enemy):
        print("Wyświetlanie interfejsu walki...")
    # Ukryj normalne przyciski akcji (np. Eksploruj, Ekwipunek, itp.)
        self.clear_action_buttons()

        # Wyświetl panel walki
        self.battle_frame.pack(pady=10)

        # self.clear_battle_frame()

    # Wyświetlenie informacji o wrogu
        self.enemy_hp_label = Label(self.battle_frame, text=f"{enemy.name} HP: {enemy.hp}", font=("Arial", 12, "bold"), fg="red")
        self.enemy_hp_label.pack()

    # Przyciski akcji związane z walką
        self.attack_button = Button(self.battle_frame, text="Atakuj", width=20, command=self.controller.player_attack)
        self.attack_button.pack(pady=5)

        self.use_potion_button = Button(self.battle_frame, text="Użyj Mikstury", width=20, command=self.controller.use_potion)
        self.use_potion_button.pack(pady=5)

        self.run_button = Button(self.battle_frame, text="Uciekaj", width=20, command=self.controller.attempt_escape)
        self.run_button.pack(pady=5)

    def update_enemy_hp(self, enemy):
        if hasattr(self, 'enemy_hp_label'):
            self.enemy_hp_label.config(text=f"{enemy.name} HP: {enemy.hp}")

    def restore_main_menu(self):
        self.clear_battle_frame()
        self.create_action_buttons()

    def create_action_buttons(self):
        self.clear_action_buttons()

        self.explore_button = Button(self.action_frame, text="Eksploruj", width=15, command=self.controller.explore)
        self.explore_button.pack(side=LEFT, padx=5)

        self.inventory_button = Button(self.action_frame, text="Ekwipunek", width=15, command=self.controller.open_inventory)
        self.inventory_button.pack(side=LEFT, padx=5)

        self.talk_button = Button(self.action_frame, text="Rozmowa", width=15, command=self.controller.talk)
        self.talk_button.pack(side=LEFT, padx=5)

        self.fight_button = Button(self.action_frame, text="Walka", width=15, command=self.controller.fight)
        self.fight_button.pack(side=LEFT, padx=5)

        self.change_location_button = Button(self.action_frame, text="Zmień Lokację", width=15, command=self.controller.change_location)
        self.change_location_button.pack(side=LEFT, padx=5)

    def show_inventory(self, inventory):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Ekwipunek")
        inventory_window.geometry("300x400")

        Label(inventory_window, text="Twój ekwipunek:", font=("Arial", 12, "bold")).pack(pady=10)

        if not inventory:
            Label(inventory_window, text="Ekwipunek jest pusty.").pack(pady=10)
            return

        for item in inventory:
            item_frame = Frame(inventory_window)
            item_frame.pack(pady=5)

            item_label = Label(item_frame, text=item.name)
            item_label.pack(side=LEFT, padx=5)

            use_button = Button(item_frame, text="Użyj", command=lambda i=item: self.controller.use_item(i))
            use_button.pack(side=RIGHT, padx=5)

    def show_npc_dialogue(self, npc):
        dialogue_window = tk.Toplevel(self.root)
        dialogue_window.title(f"Rozmowa z {npc.name}")
        dialogue_window.geometry("400x300")

        Label(dialogue_window, text=f"{npc.name} mówi:", font=("Arial", 12, "bold")).pack(pady=10)

        dialogue_text = Text(dialogue_window, wrap="word", height=10, state="normal")
        dialogue_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        dialogue_text.insert(END, npc.dialogue)
        dialogue_text.config(state="disabled")

        close_button = Button(dialogue_window, text="Zamknij", command=dialogue_window.destroy)
        close_button.pack(pady=10)