import tkinter as tk
from tkinter import messagebox
import os
import json

SAVE_DIR = "data/saved_games"

class NameHeroScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")  # Pustynne tło
        self.controller = controller

        # Nagłówek
        tk.Label(
            self,
            text="Nadaj imię swojemu bohaterowi",
            font=("Georgia", 16, "bold"),
            bg="#f5ecd9",
            fg="#4d3319"
        ).pack(pady=30)

        # Pole tekstowe
        self.entry_name = tk.Entry(
            self,
            font=("Georgia", 14),
            width=30,
            justify="center",
            relief="groove",
            bd=3
        )
        self.entry_name.pack(pady=10)

        # Przycisk zapisu (bez ramki)
        btn_zapisz = tk.Button(
            self,
            text="Zapisz",
            font=("Georgia", 12, "bold"),
            bg="#996633",
            fg="#fef9f3",
            activebackground="#b37843",
            relief="raised",
            borderwidth=3,
            width=15,
            command=self.save_hero
        )
        btn_zapisz.pack(pady=10)

    def save_hero(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Błąd", "Wpisz imię bohatera!")
            return

        filename = f"{name}.json"
        filepath = os.path.join(SAVE_DIR, filename)

        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        game_mode = self.controller.get_game_mode() # dodaje game_mode :)

        initial_data = {
            "name": name,
            "mode": game_mode,  # ZAPISUJEMY TRYB
            "stats": {
                "punkty_życia": 0,
                "siła": 0,
                "obrona": 0
            },
            "hp": 0,
            "exp": 0,
            "level": 1
        }

        with open(filepath, 'w') as f:
            json.dump(initial_data, f, indent=4)

        self.controller.set_hero_name(name)
        game_mode = self.controller.get_game_mode()
        if game_mode == "klasyczne":
            self.controller.show_frame("StatAllocationScreen")
        else:
            self.controller.show_frame("MainGameScreen")
