import tkinter as tk
from screens.game_mode import GameModeScreen
from screens.new_or_load import NewOrLoadScreen
from screens.name_hero import NameHeroScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lukos RPG")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg="#f5ecd9")  # Ustawienie pustynnego tła

        self.container = tk.Frame(self, bg="#f5ecd9")  # Ustawienie tła kontenera
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.hero_name = None
        self.game_mode = None

        self.init_frames()

    def init_frames(self):
        from screens.stat_allocation import StatAllocationScreen
        from screens.main_game import MainGameScreen
        from screens.event_screen import EventScreen
        from screens.level_up_screen import LevelUpScreen

        for F in (
            GameModeScreen,
            NewOrLoadScreen,
            NameHeroScreen,
            StatAllocationScreen,
            MainGameScreen,
            EventScreen,
            LevelUpScreen
        ):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("GameModeScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, "update_display"):
            frame.update_display()
        frame.tkraise()

    def set_hero_name(self, name):
        self.hero_name = name

    def get_hero_name(self):
        return self.hero_name

    def set_game_mode(self, mode):
        self.game_mode = mode

    def get_game_mode(self):
        return self.game_mode

if __name__ == "__main__":
    app = App()
    app.mainloop()
