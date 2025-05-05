import tkinter as tk
from tkinter import ttk

class GameScreen:
    def __init__(self, root, player, controller):
        self.root = root
        self.player = player
        self.controller = controller
        self.create_screen()

    def create_screen(self):
        # Main frame
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill="both", expand=True)
        
        # left
        self.left_frame = tk.Frame(self.game_frame, width=300, height=700, bg="lightgray")
        self.left_frame.pack(side="left", fill="both", expand=True)     
        
        # midle
        self.center_frame = tk.Frame(self.game_frame, width=200, height=700)
        self.center_frame.pack(side="left", fill="both", expand=True)
        
        # right
        self.right_frame = tk.Frame(self.game_frame, width=400, height=700, bg="lightblue")
        self.right_frame.pack(side="left", fill="both", expand=True)
        
        
        self.create_start_action_buttons()
        self.create_player_info()
        # self.create_enemy_info()
        
        

    def create_enemy_info(self):
        enemy_info = f"""
            Enemy {self.enemy.name}
            HP: {self.enemy.hp}
            Attack: {self.enemy.attack}
            Defense: {self.enemy.defense}
            EXP Reward: {self.enemy.exp}
            Description: {self.enemy.description}"""

        self.enemy_label = tk.Label(self.left_frame, text=enemy_info, font=("Arial", 14))
        self.enemy_label.pack(pady=20)

    def create_player_info(self):
        player_info = f"""
            Name: {self.player.name},
            Class: {self.player.class_name},
            HP: {self.player.hp}, 
            SP: {self.player.sp}, 
            Attack: {self.player.attack}, 
            Defence: {self.player.defense}"""
        self.player_label = tk.Label(self.right_frame, text=player_info, font=("Arial", 14))
        self.player_label.pack(pady=20)

    def create_start_action_buttons(self):
        castle_btn = tk.Button(self.center_frame, text="Castle", command=self.controller.go_to_castle, width=20)
        gate_btn = tk.Button(self.center_frame, text="Gateway", command=self.controller.go_to_gate, width=20)
        forest_btn = tk.Button(self.center_frame, text="Forest", command=self.controller.go_to_forest, width=20)

        castle_btn.pack(pady=10)
        gate_btn.pack(pady=10)
        forest_btn.pack(pady=10)

    def create_castle_screen(self):
        pass

    def create_forest_screen(self):
        pass

    def create_gate_screen(self):
        pass