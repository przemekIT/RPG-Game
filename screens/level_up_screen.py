import tkinter as tk
import json
import os

SAVE_DIR = "data/saved_games"

class LevelUpScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")  # Pustynne tło
        self.controller = controller

        # Nagłówek
        tk.Label(
            self,
            text="Awans! Masz 1 punkt do rozdania!",
            font=("Georgia", 16, "bold"),
            bg="#f5ecd9",
            fg="#4d3319"
        ).pack(pady=20)

        # Ramka z przyciskami i obramowaniem
        self.buttons_frame = tk.Frame(self, bg="#f5ecd9", highlightbackground="#996633", highlightthickness=2)
        self.buttons_frame.pack(pady=15)

        # Przycisk: +1 do życia
        self.create_stat_button("punkty_życia", "Punkty życia")

        # Przycisk: +1 do siły
        self.create_stat_button("siła", "Siła")

        # Przycisk: +1 do obrony
        self.create_stat_button("obrona", "Obrona")

    # Tworzenie pojedynczego przycisku
    def create_stat_button(self, stat_key, label):
        tk.Button(
            self.buttons_frame,
            text=label,
            font=("Georgia", 12, "bold"),
            bg="#996633",
            fg="#fef9f3",
            activebackground="#b37843",
            relief="raised",
            borderwidth=3,
            width=20,
            command=lambda: self.allocate_point(stat_key)
        ).pack(pady=8)

    # Przypisanie punktu do wybranej statystyki
    def allocate_point(self, stat_key):
        name = self.controller.get_hero_name()
        filepath = os.path.join(SAVE_DIR, f"{name}.json")
        with open(filepath, 'r') as f:
            data = json.load(f)

        data["stats"][stat_key] += 1
        if stat_key == "punkty_życia":
            data["hp"] = data["stats"]["punkty_życia"] * 10

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        self.controller.show_frame("MainGameScreen")
