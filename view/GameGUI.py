import tkinter as tk
from typing import Any, Dict

class GameGUI:
    def __init__(self, root: tk.Tk, data: Dict[str, Any], controller: Any) -> None:
        self.root: tk.Tk = root
        self.data: Dict[str, Any] = data
        self.controller: Any = controller

        self.setup_window()

        self.main_frame = tk.Frame(self.root, bg=self.root["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_menu()

    def setup_window(self) -> None:
        window_data = self.data.get("Window")
        if not window_data:
            raise ValueError("Window configuration not found in data.")
        
        self.root.title(window_data["title"])
        self.root.geometry(window_data["geometry"])
        self.root.configure(bg=window_data["bg"])

        self.root.resizable(False, False)

    def clear_screen(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_main_menu(self) -> None:
        self.clear_screen() 

        frame = tk.Frame(self.main_frame, bg=self.root["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(
            frame,
            text="Legends of the Castle",
            font=("Georgia", 32, "bold"),
            fg="#f0e6d6",
            bg=self.root["bg"]
        )
        title_label.pack(pady=(0, 50))

        button_style = {
            "bg": "#4b3f2f",
            "fg": "#f0e6d6",
            "activebackground": "#6a5b45",
            "activeforeground": "#ffffff",
            "font": ("Georgia", 16, "bold"),
            "relief": "raised",
            "bd": 3,
            "width": 20,
            "height": 2,
            "padx": 5,
            "pady": 5
        }

        new_game = tk.Button(frame, text="New Game", command=self.controller.new_game, **button_style)
        load_game = tk.Button(frame, text="Load Game", command=self.controller.load_game, **button_style) # command=self.controller.load_game,
        exit_game = tk.Button(frame, text="Exit", command=self.root.quit, **button_style)

        new_game.pack(pady=15)
        load_game.pack(pady=15)
        exit_game.pack(pady=15)
