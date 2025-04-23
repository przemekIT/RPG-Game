import tkinter as tk
from tkinter import messagebox
import os
import json

SAVE_DIR = "data/saved_games"

class NewOrLoadScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")
        self.controller = controller

        tk.Label(self, text="Rozpocznij grę", font=("Georgia", 18, "bold"),
                 bg="#f5ecd9", fg="#4d3319").pack(pady=30)

        # Nowa gra
        btn_nowa = tk.Button(self, text="Nowa Przygoda", font=("Georgia", 12, "bold"),
                             bg="#996633", fg="#fef9f3", activebackground="#b37843",
                             relief="raised", borderwidth=3, width=20,
                             command=self.new_game)
        btn_nowa.pack(pady=10)

        # Wczytaj zapis
        btn_pokaz = tk.Button(self, text="Wczytaj Zapis", font=("Georgia", 12, "bold"),
                              bg="#996633", fg="#fef9f3", activebackground="#b37843",
                              relief="raised", borderwidth=3, width=20,
                              command=self.toggle_listbox)
        btn_pokaz.pack(pady=10)

        # Ramka z listą i przyciskiem ładowania (na razie ukryta)
        self.load_frame = tk.Frame(self, bg="#f5ecd9")

        tk.Label(self.load_frame, text="Wybierz zapis:", font=("Georgia", 12),
                 bg="#f5ecd9", fg="#4d3319").pack()

        self.save_listbox = tk.Listbox(self.load_frame, font=("Georgia", 12),
                                       width=30, height=5)
        self.save_listbox.pack(pady=5)

        btn_wczytaj = tk.Button(self.load_frame, text="Potwierdź", font=("Georgia", 12, "bold"),
                                bg="#996633", fg="#fef9f3", activebackground="#b37843",
                                relief="raised", borderwidth=3, width=20,
                                command=self.load_game)
        btn_wczytaj.pack(pady=5)

    def toggle_listbox(self):
        if self.load_frame.winfo_ismapped():
            self.load_frame.pack_forget()
        else:
            self.refresh_save_list()
            self.load_frame.pack(pady=10)

    def refresh_save_list(self):
        self.save_listbox.delete(0, tk.END)
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
        for file in files:
            self.save_listbox.insert(tk.END, file)

    def new_game(self):
        self.controller.show_frame("NameHeroScreen")

    def load_game(self):
        selected = self.save_listbox.curselection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Wybierz zapis z listy.")
            return

        filename = self.save_listbox.get(selected[0])
        filepath = os.path.join(SAVE_DIR, filename)

        try:
            with open(filepath, 'r') as f:
                dane = json.load(f)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku: {e}")
            return

        # Weryfikacja zgodności trybu gry
        current_mode = self.controller.get_game_mode()
        saved_mode = dane.get("mode")
        if saved_mode and saved_mode != current_mode:
            messagebox.showerror("Niekompatybilny zapis", "Ten zapis pochodzi z innego trybu gry.")
            return

        self.controller.set_hero_name(dane["name"])
        self.controller.show_frame("MainGameScreen")
