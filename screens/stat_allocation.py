import tkinter as tk
import json
import os

SAVE_DIR = "data/saved_games"

class StatAllocationScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")  # pustynne tło
        self.controller = controller

        self.remaining_points = 5
        self.stats = {
            "punkty_życia": 0,
            "siła": 0,
            "obrona": 0
        }

        # Nagłówek
        tk.Label(
            self,
            text="Przydziel 5 punktów",
            font=("Georgia", 16, "bold"),
            bg="#f5ecd9",
            fg="#4d3319"
        ).pack(pady=20)

        # Ilość dostępnych punktów
        self.points_label = tk.Label(
            self,
            text=f"Pozostałe punkty: {self.remaining_points}",
            font=("Georgia", 12),
            bg="#f5ecd9",
            fg="#4d3319"
        )
        self.points_label.pack(pady=5)

        # Ramka z obramowaniem
        self.stats_frame = tk.Frame(self, bg="#f5ecd9", highlightbackground="#996633", highlightthickness=2)
        self.stats_frame.pack(pady=10)

        # Statystyki do modyfikacji
        self.entries = {}
        for stat in self.stats:
            self.create_stat_row(stat)

        # Przycisk zapisania wyboru
        save_button = tk.Button(
            self,
            text="Zapisz",
            font=("Georgia", 12, "bold"),
            bg="#996633",
            fg="#fef9f3",
            activebackground="#b37843",
            relief="raised",
            borderwidth=3,
            command=self.save_stats
        )
        save_button.pack(pady=20)

    def create_stat_row(self, stat_key):
        row = tk.Frame(self.stats_frame, bg="#f5ecd9")
        row.pack(pady=5)

        # Nazwa statystyki
        tk.Label(row, text=stat_key.replace("_", " ").capitalize(), font=("Georgia", 12), width=15, bg="#f5ecd9", anchor="w").pack(side="left")

        # Przycisk -
        tk.Button(row, text="-", font=("Georgia", 10), command=lambda s=stat_key: self.update_stat(s, -1)).pack(side="left", padx=5)

        # Pole wyświetlania wartości
        val = tk.Label(row, text="0", font=("Georgia", 12), width=3, bg="#f5ecd9")
        val.pack(side="left")
        self.entries[stat_key] = val

        # Przycisk +
        tk.Button(row, text="+", font=("Georgia", 10), command=lambda s=stat_key: self.update_stat(s, 1)).pack(side="left", padx=5)

    def update_stat(self, stat_key, delta):
        new_val = self.stats[stat_key] + delta

        if delta == 1 and self.remaining_points == 0:
            return
        if delta == -1 and new_val < 0:
            return

        self.stats[stat_key] = new_val
        self.entries[stat_key].config(text=str(new_val))
        self.remaining_points -= delta
        self.points_label.config(text=f"Pozostałe punkty: {self.remaining_points}")

    def save_stats(self):
        if self.remaining_points > 0:
            return  # nie pozwól zapisać, jeśli punkty nie są przydzielone

        name = self.controller.get_hero_name()
        filepath = os.path.join(SAVE_DIR, f"{name}.json")

        with open(filepath, "r") as f:
            data = json.load(f)

        data["stats"] = self.stats
        data["hp"] = self.stats["punkty_życia"] * 10

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        self.controller.show_frame("MainGameScreen")
