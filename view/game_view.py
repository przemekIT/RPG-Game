import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Label, Button, Text, Scrollbar, END, LEFT, RIGHT, BOTH, Y

# class GameView:
#     def __init__(self, root, controller):
#         self.root = root
#         self.controller = controller

#         # Przykładowe elementy GUI
#         self.label = Label(self.root, text="Witaj w grze!")
#         self.label.pack()

#         # Przykładowy przycisk, który uruchamia eksplorację
#         self.explore_button = Button(
#             self.root, text="Eksploruj", command=self.controller.explore
#         )
#         self.explore_button.pack()

#     def display_location(self, location):
#         # Funkcja aktualizująca widok lokalizacji
#         self.label.config(text=f"Jesteś w: {location.name}")

#     def update_stats(self, player):
#         # Funkcja aktualizująca dane o postaci (np. HP)
#         self.label.config(
#             text=f"{player.name} - HP: {player.hp} - Poziom: {player.level}"
#         )

#     def show_message(self, message):
#         # Funkcja do wyświetlania wiadomości
#         self.label.config(text=message)


# 2
class GameView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # === Dodajemy panel na przyciski ===
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=10)
        # === Przycisk zmien lokacje ===
        self.move_button = Button(
            self.button_frame,
            text="Zmień lokację",
            command=self.controller.change_location,
        )
        self.move_button.pack(side="left", padx=5)

        # self.explore_button = Button(
        #     self.button_frame, text="Eksploruj", command=self.controller.explore
        # )
        # self.explore_button.pack(side="left", padx=5)

        # === Panel statystyk ===
        self.stats_label = Label(
            self.root, text="Statystyki gracza", anchor="w", justify="left"
        )
        self.stats_label.pack(fill="x")

        # === Opis lokacji ===
        self.location_label = Label(
            self.root, text="Lokalizacja: ???", font=("Arial", 12, "bold")
        )
        self.location_label.pack(pady=10)

        # === Log gry ===
        self.log_frame = Frame(self.root)
        self.log_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.log_text = Text(self.log_frame, wrap="word", height=10, state="disabled")
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        # === Menu akcji ===
        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=10)

        self.explore_button = Button(
            self.button_frame, text="Eksploruj", command=self.controller.explore
        )
        self.explore_button.pack(side=LEFT, padx=5)

        self.inventory_button = Button(
            self.button_frame, text="Ekwipunek", command=self.controller.open_inventory
        )
        self.inventory_button.pack(side=LEFT, padx=5)

        self.talk_button = Button(
            self.button_frame, text="Rozmowa", command=self.controller.talk
        )
        self.talk_button.pack(side=LEFT, padx=5)

        self.fight_button = Button(
            self.button_frame, text="Walka", command=self.controller.fight
        )
        self.fight_button.pack(side=LEFT, padx=5)

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

    def show_fight_interface(self, enemy):
        self.clear_action_buttons()
        self.attack_button = Button(self.button_frame, text="Atakuj", command=lambda: self.controller.attack(enemy))
        self.attack_button.pack(side=LEFT, padx=5)

        self.potion_button = Button(self.button_frame, text="Uzyj mikstury", command=self.controller.use_potion)
        self.potion_button.pack(side=LEFT, padx=5)
