import tkinter as tk
class GameGUI:
    def __init__(self, root, data, controller):
        self.root = root
        self.data = data
        self.controller = controller

        self.setup_window()

        self.main_frame = tk.Frame(self.root, bg=self.root["bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_menu()

    def setup_window(self):
        window_data = self.data.get("Window")
        if not window_data:
            raise ValueError("Window configuration not found in data.")
        
        self.root.title(window_data["title"])
        self.root.geometry(window_data["geometry"])
        self.root.configure(bg=window_data["bg"])

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_screen() 

        frame = tk.Frame(self.main_frame, bg=self.root["bg"])
        frame.place(relx=0.5, rely=0.5,anchor="center")

        new_game = tk.Button(frame, text="New Game", command=self.controller.new_game, width=20, height=2)
        load_game = tk.Button(frame, text="Load Game", width=20, height=2)
        exit_game = tk.Button(frame, text="Exit", width=20, height=2)

        new_game.pack(pady=20)
        load_game.pack(pady=20)
        exit_game.pack(pady=20)
