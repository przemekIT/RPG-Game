import tkinter as tk
import random
import json
import os
from tkinter import messagebox

SAVE_DIR = "data/saved_games"

class EventScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")  # Pustynne tło
        self.controller = controller
        self.direction = None

        self.text_area = tk.Text(self, wrap="word", height=10, width=70,
                                 font=("Georgia", 12), bg="#fff9ec", relief="sunken", bd=3)
        self.text_area.pack(pady=10)

        # Pole wpisu do użycia tylko w matematycznym trybie
        self.input_entry = tk.Entry(self, font=("Georgia", 12), width=30,
                                    justify="center", bg="#fef9f3", relief="groove")

        # Przycisk WALKA – widoczny zawsze
        self.submit_button = tk.Button(self, text="Walka", font=("Georgia", 12, "bold"),
                                       bg="#996633", fg="#fef9f3", activebackground="#b37843",
                                       relief="raised", borderwidth=3, command=self.process_input)
        self.submit_button.pack(pady=5)

        self.result_label = tk.Label(self, text="", font=("Georgia", 12),
                                     bg="#f5ecd9", fg="#4d3319")
        self.result_label.pack(pady=5)

        self.back_button = tk.Button(self, text="Powrót", font=("Georgia", 12, "bold"),
                                     bg="#996633", fg="#fef9f3", activebackground="#b37843",
                                     relief="raised", borderwidth=3,
                                     command=self.return_to_main)
        self.back_button.pack(pady=10)

    def set_direction(self, direction):
        self.direction = direction
        self.generate_event()

    def generate_event(self):
        self.text_area.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.input_entry.delete(0, tk.END)
        self.input_entry.pack_forget()

        game_mode = self.controller.get_game_mode()

        phrases = [
            "Idziesz przez mglisty las...",
            "Wchodzisz do pradawnej świątyni...",
            "Przekraczasz ruiny zamku...",
            "znajdujesz ruiny zamku...",
            "Przekraczając rzekę...",
            "Znajdujesz jaskinie...",
            "Dostrzegasz ognisko przy szkalu",
            "Ulewa przygnała Cię do gospody",
            "Jesteś na jarmarku",
            "Przemieżasz pasma górskie",
            "Wchodzisz na polane",
            "znajdujesz sie przed bramą warownii",
            "Wędrujesz przez pustkowie"
            "Mijasz szlak kupiecki"
            
        ]
        stories = [
            "Spotykasz strażnika wiedzy.",
            "Dostrzegasz runiczny kamień z zagadką.",
            "Wyłania się zakapturzona postać...",
            "Nagle słyszysz trzask gałęzi w krzakach...",
            "W oddali dostrzegasz poruszającą się sylwetkę...",
            "Twoją uwagę przykuwa dziwny dźwięk...",
            "Ktoś lub coś Cię obserwuje...",
            "Cisza nagle staje się przytłaczająca...",
            "Czujesz, że coś jest nie tak...",
            "Na ziemi widzisz świeże ślady stóp...",
            "Coś przemknęło między drzewami...",
            "Z ziemi unosi się gęsta mgła...",
            "Wyczuwasz zapach dymu i spalenizny...",
            "Słyszysz odgłosy walki w oddali...",
            "Na twojej drodze pojawia się sylwetka nie wygląda przyjaźnie...",
            "Nagle coś przelatuje obok twojej głowy...",
            "Słychać ciężkie kroki, które szybko się zbliżają..."


        ]
        enemies = [
            "Mistrz Algebrion",
            "Mag Dzielax",
            "Zakonnik Mnożator",
            "Bandyta",
            "Uzbrojony Ork",
            "Troll",
            "Wilk",
            "Niedziwedź",
            "Dzikie Psy",
            "Rycerz Gwardii królewskiej",
            "Najemnik",
            "Barbażyńca"
        ]

        phrase = random.choice(phrases)
        story = random.choice(stories)
        enemy = random.choice(enemies)

        self.text_area.insert(tk.END, f"{phrase}\n{story}\nPrzeciwnik: {enemy}\n")

        if game_mode == "matematyczne":
            self.generate_math_challenge()
            self.input_entry.pack(pady=5)

        else:
            self.generate_classic_battle()

    def generate_math_challenge(self):
        op = random.choice(["*", "/"])
        if op == "*":
            a = random.randint(1, 11)
            b = random.randint(1, 11)
            self.correct_answer = a * b
            question = f"Ile to {a} x {b}?"
        else:
            a = random.randint(1, 10)
            b = a * random.randint(1, 10)
            self.correct_answer = b // a
            question = f"Ile to {b} ÷ {a}?"

        self.text_area.insert(tk.END, f"\n{question}")

    def generate_classic_battle(self):
        name = self.controller.get_hero_name()
        filepath = os.path.join(SAVE_DIR, f"{name}.json")
        with open(filepath, 'r') as f:
            data = json.load(f)

        strength = data["stats"].get("siła", 2)
        level = data.get("level", 1)

        # Skalowanie miecza
        base_weapon = 2
        upgrade_factor = 2 ** (level // 5)
        weapon_value = base_weapon * upgrade_factor

        attack_roll = random.randint(1, 6)
        self.attack_power = int(strength / 2) + weapon_value + attack_roll

        enemy_level = level
        defense_roll = random.randint(1, 6)
        self.enemy_defense = defense_roll + enemy_level + 2

        self.text_area.insert(tk.END, f"\nTwój atak: {self.attack_power}")
        self.text_area.insert(tk.END, f"\nObrona przeciwnika: {self.enemy_defense}")

        
    def process_input(self):
        game_mode = self.controller.get_game_mode()
        name = self.controller.get_hero_name()
        filepath = os.path.join(SAVE_DIR, f"{name}.json")
        with open(filepath, 'r') as f:
            data = json.load(f)

        if game_mode == "matematyczne":
            try:
                answer = int(self.input_entry.get())
                if answer == self.correct_answer:
                    self.result_label.config(text=" Poprawna odpowiedź! Zdobywasz 5 XP.")
                    data["exp"] += 5
                else:
                    self.result_label.config(text=" Błędna odpowiedź. Tracisz 5 HP.")
                    data["hp"] -= 5
                    data["errors"] = data.get("errors", 0) + 1
                    if data["errors"] >= 5:
                        os.remove(filepath)
                        messagebox.showinfo("Umarłeś", "Umarłeś. Zacznij od nowa.")
                        self.controller.show_frame("NewOrLoadScreen")
                        return
            except ValueError:
                self.result_label.config(text=" Wprowadź poprawną liczbę.")
                return
        else:
            if self.attack_power > self.enemy_defense:
                self.result_label.config(text=" Wygrałeś walkę! Zdobywasz 5 XP.")
                data["exp"] += 5
            else:
                self.result_label.config(text=" Przegrałeś walkę. Tracisz 5 HP.")
                data["hp"] -= 5

        if data["hp"] <= 0:
            os.remove(filepath)
            messagebox.showinfo("Umarłeś", "Umarłeś. Zacznij od nowa.")
            self.controller.show_frame("NewOrLoadScreen")
            return

        if data["exp"] >= data["level"] * 15:
            data["level"] += 1
            data["exp"] = 0
            data["hp"] = data["stats"]["punkty_życia"] * 10
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo("Awans!", f"Osiągnąłeś poziom {data['level']}! Przydziel 1 punkt statystyk.")
            self.controller.show_frame("LevelUpScreen")
        else:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)

    def return_to_main(self):
        self.controller.show_frame("MainGameScreen")
