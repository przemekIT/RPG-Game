import tkinter as tk

class GameModeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f5ecd9")
        self.controller = controller

        # Centrum ekranu
        center_frame = tk.Frame(self, bg="#f5ecd9")
        center_frame.pack(expand=True)

        # Nagłówek
        tk.Label(
            center_frame,
            text="Wybierz tryb gry",
            font=("Georgia", 18, "bold"),
            bg="#f5ecd9",
            fg="#4d3319"
        ).pack(pady=(20, 30))

        # Przycisk: RPG Klasyczne
        btn_klasyczne = tk.Button(
            center_frame,
            text=" RPG Klasyczne",
            font=("Georgia", 12, "bold"),
            bg="#996633",
            fg="#fef9f3",
            activebackground="#b37843",
            relief="raised",
            borderwidth=3,
            padx=20,
            pady=5,
            command=self.choose_classic
        )
        btn_klasyczne.pack(pady=10)

        # Przycisk: RPG Matematyczne
        btn_matematyczne = tk.Button(
            center_frame,
            text=" RPG Matematyczne",
            font=("Georgia", 12, "bold"),
            bg="#996633",
            fg="#fef9f3",
            activebackground="#b37843",
            relief="raised",
            borderwidth=3,
            padx=20,
            pady=5,
            command=self.choose_math
        )
        btn_matematyczne.pack(pady=10)

    def choose_classic(self):
        self.controller.set_game_mode("klasyczne")
        self.controller.show_frame("NewOrLoadScreen")

    def choose_math(self):
        self.controller.set_game_mode("matematyczne")
        self.controller.show_frame("NewOrLoadScreen")
