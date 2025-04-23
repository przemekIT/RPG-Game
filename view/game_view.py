import tkinter as tk
from tkinter import Tk, Label, Button
from tkinter import ttk

from tkinter import Tk, Label, Button


class GameView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Przykładowe elementy GUI
        self.label = Label(self.root, text="Witaj w grze!")
        self.label.pack()

        # Przykładowy przycisk, który uruchamia eksplorację
        self.explore_button = Button(
            self.root, text="Eksploruj", command=self.controller.explore
        )
        self.explore_button.pack()

    def display_location(self, location):
        # Funkcja aktualizująca widok lokalizacji
        self.label.config(text=f"Jesteś w: {location.name}")

    def update_stats(self, player):
        # Funkcja aktualizująca dane o postaci (np. HP)
        self.label.config(
            text=f"{player.name} - HP: {player.hp} - Poziom: {player.level}"
        )

    def show_message(self, message):
        # Funkcja do wyświetlania wiadomości
        self.label.config(text=message)


# class GameView:
#     def __init__(self, root, controller):
#         self.root = root
#         self.controller = controller

#         self.stats_frame = tk.Frame(root)
#         self.stats_frame.pack()

#         self.location_frame = tk.Frame(root)
#         self.location_frame.pack()

#         self.actions_frame = tk.Frame(root)
#         self.actions_frame.pack()

#         self.stats_label = tk.Label(self.stats_frame, text="Statystyki gracza")
#         self.stats_label.pack()

#         self.location_desc = tk.Label(self.location_frame, text="Opis lokacji")
#         self.location_desc.pack()

#         self.explore_button = tk.Button(
#             self.actions_frame, text="Eksploruj", command=self.controller.explore
#         )
#         self.explore_button.pack()

#         self.message_label = tk.Label(self.actions_frame, text="")
#         self.message_label.pack()

#     def update_stats(self, player):
#         self.stats_label.config(
#             text=f"{player.name} | HP: {player.hp} | EXP: {player.exp}"
#         )

#     def display_location(self, location):
#         self.location_desc.config(text=location.describe())

#     def show_message(self, message):
#         self.message_label.config(text=message)
