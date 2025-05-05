import tkinter as tk
from view.GameGUI import GameGUI
from view.CreateGame import CreateGame
from view.GameScreen import GameScreen
from model.GameCharacter import GameCharacter
from model.player import Player
import json
from pathlib import Path

class GameController:
    def __init__(self):
        self.data_player = self.load_data("assets/characters.json")
        self.dataGUI = self.load_data("assets/mainGUI.json")
        self.root = tk.Tk()
        self.gui = GameGUI(self.root, self.dataGUI, self)
        self.characters = GameCharacter(self.data_player)

    def load_data(self, file):
        basePath = Path(__file__).parent
        file_path = (basePath / ".." / file ).resolve()
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def new_game(self):
        self.gui.clear_screen()
        
        self.new_create = CreateGame(self.gui.main_frame, self)

    def create_character(self, name, char_class):
        self.player = self.characters.create_player(name, char_class)
        self.enemys = self.characters.create_enemy()

        # self.gui.clear_screen()

        self.start_game()

    def start_game(self):
        self.gui.clear_screen()
        self.game_screen = GameScreen(self.root, self.player, self)

    def go_to_forest(self):
        pass

    def go_to_castle(self):
        pass

    def go_to_gate(self):
        pass

    def run(self):
        # player = self.characters.get_player()
        self.root.mainloop()
