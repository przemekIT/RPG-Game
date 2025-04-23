import tkinter as tk
from tkinter import ttk
import json
import os
from PIL import Image, ImageTk
from utils.equipment import update_equipment  # Dodajemy import z nazwami broni/zbroi

SAVE_DIR = "data/saved_games"

class MainGameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")  # pustynne tło
        self.controller = controller

        self.hp_var = tk.IntVar()
        self.xp_var = tk.IntVar()
        self.max_xp = 15
        self.level_var = tk.IntVar()

        # Nagłówek
        tk.Label(self, text="Twoja Przygoda", font=("Georgia", 16, "bold"),
                 bg="#f5ecd9", fg="#4d3319").pack(pady=10)

        # Ramka z ekwipunkiem (3x2)
        eq_frame = tk.Frame(self, bg="#f5ecd9")
        eq_frame.pack(pady=10)

        # === Nazwy nad grafikami ===
        self.weapon_name_label = tk.Label(eq_frame, text="", font=("Georgia", 10, "italic"),
                                          bg="#f5ecd9", fg="#4d3319")
        self.weapon_name_label.grid(row=0, column=0, padx=30)

        self.armor_name_label = tk.Label(eq_frame, text="", font=("Georgia", 10, "italic"),
                                         bg="#f5ecd9", fg="#4d3319")
        self.armor_name_label.grid(row=0, column=1, padx=30)

        # === Obrazki ===
        sword_img = Image.open("assets/sword.png").resize((80, 80))
        self.tk_sword = ImageTk.PhotoImage(sword_img)
        tk.Label(eq_frame, image=self.tk_sword, bg="#f5ecd9").grid(row=1, column=0, padx=30)

        armor_img = Image.open("assets/armor.png").resize((80, 80))
        self.tk_armor = ImageTk.PhotoImage(armor_img)
        tk.Label(eq_frame, image=self.tk_armor, bg="#f5ecd9").grid(row=1, column=1, padx=30)

        # === Formuły ===
        self.attack_info = tk.Label(eq_frame, text="", font=("Georgia", 10),
                                    bg="#f5ecd9", fg="#4d3319")
        self.attack_info.grid(row=2, column=0)

        self.defense_info = tk.Label(eq_frame, text="", font=("Georgia", 10),
                                     bg="#f5ecd9", fg="#4d3319")
        self.defense_info.grid(row=2, column=1)

        # === Potencjały ===
        self.attack_result = tk.Label(eq_frame, text="", font=("Georgia", 11, "bold"),
                                      bg="#f5ecd9", fg="#332211")
        self.attack_result.grid(row=3, column=0, pady=(5, 15))

        self.defense_result = tk.Label(eq_frame, text="", font=("Georgia", 11, "bold"),
                                       bg="#f5ecd9", fg="#332211")
        self.defense_result.grid(row=3, column=1, pady=(5, 15))

        # === Pasek HP ===
        tk.Label(self, text="HP", font=("Georgia", 10, "bold"),
                 bg="#f5ecd9", fg="#4d3319").pack()
        self.hp_bar = ttk.Progressbar(self, maximum=100, variable=self.hp_var, length=300)
        self.hp_bar.pack(pady=5)

        # === Pasek XP ===
        tk.Label(self, text="XP", font=("Georgia", 10, "bold"),
                 bg="#f5ecd9", fg="#4d3319").pack()
        self.xp_bar = ttk.Progressbar(self, maximum=self.max_xp, variable=self.xp_var, length=300)
        self.xp_bar.pack(pady=5)

        # === Poziom ===
        self.level_label = tk.Label(self, text="Poziom: 1", font=("Georgia", 10),
                                    bg="#f5ecd9", fg="#4d3319")
        self.level_label.pack(pady=5)

        # === Kierunki ===
        directions = ["LEWO", "PROSTO", "PRAWO"]
        dir_frame = tk.Frame(self, bg="#f5ecd9")
        dir_frame.pack(pady=15)

        for direction in directions:
            tk.Button(dir_frame, text=direction, width=10,
                      font=("Georgia", 10, "bold"),
                      bg="#996633", fg="#fef9f3", activebackground="#b37843",
                      relief="raised", borderwidth=3,
                      command=lambda d=direction: self.go_to_event(d)).pack(side="left", padx=10)

    def go_to_event(self, direction):
        self.controller.frames["EventScreen"].set_direction(direction)
        self.controller.show_frame("EventScreen")

    def update_display(self):
        name = self.controller.get_hero_name()
        filepath = os.path.join(SAVE_DIR, f"{name}.json")
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Ustawienia XP i HP
        self.hp_var.set(data["hp"])
        xp = data["exp"]
        lvl = data["level"]
        self.level_var.set(lvl)

        self.max_xp = lvl * 15
        self.xp_bar.config(maximum=self.max_xp)
        self.xp_var.set(xp)
        self.level_label.config(text=f"Poziom: {lvl}")

        # Statystyki i skalowanie
        strength = data["stats"].get("siła", 2)
        dexterity = data["stats"].get("zręczność", 2)
        base_weapon = 2
        base_armor = 3

        upgrade_factor = 2 ** (lvl // 5)
        weapon_value = base_weapon * upgrade_factor
        armor_value = base_armor * upgrade_factor

        # Obliczenia potencjału
        attack_power = int(strength / 2) + weapon_value
        defense_power = int((dexterity + armor_value) / 4)

        # Aktualizacja GUI
        self.attack_info.config(text=f"Siła({strength}) + Miecz({weapon_value})")
        self.attack_result.config(text=f"Potencjał Ataku: {attack_power}")

        self.defense_info.config(text=f"Zręczność({dexterity}) + Zbroja({armor_value}) / 4")
        self.defense_result.config(text=f"Potencjał Obrony: {defense_power}")

        # === Nazwy sprzętu ===
        weapon_name, armor_name = update_equipment(lvl)
        self.weapon_name_label.config(text=weapon_name)
        self.armor_name_label.config(text=armor_name)
