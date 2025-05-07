import tkinter as tk
from tkinter import ttk

class GameScreen:
    def __init__(self, root, controller, dataGui):
        self.root = root
        self.controller = controller
        self.event_log = None
        self.dataGui = dataGui.get("Window")
        self.create_screen()
        
    def create_event_log(self):
        log_border = tk.Frame(self.center_log_frame, bg=self.dataGui["bg"], bd=2, relief="groove")
        log_border.pack(fill="both", expand=True, padx=5, pady=5)

        self.event_log = tk.Text(log_border, height=10, state="disabled",
                                wrap="word", bg=self.dataGui["bg"], relief="flat", bd=0,
                                font=("Arial", 11))
        self.event_log.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(log_border, command=self.event_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.event_log.config(yscrollcommand=scrollbar.set)

    def update_event_log(self, message):
        self.event_log.config(state="normal")
        self.event_log.insert("end", message + "\n")
        self.event_log.see("end")
        self.event_log.config(state="disabled")

    def create_screen(self):
        self.game_frame = tk.Frame(self.root, bg=self.dataGui["bg"])
        self.game_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.game_frame, width=400, height=700, bg=self.dataGui["bg"])
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        self.left_frame.pack_propagate(False)

        self.center_frame = tk.Frame(self.game_frame, width=300, height=700, bg=self.dataGui["bg"])
        self.center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.center_frame.pack_propagate(False)

        self.center_buttons_frame = tk.Frame(self.center_frame, bg=self.dataGui["bg"])
        self.center_buttons_frame.pack(side="top", pady=40)

        self.center_log_frame = tk.Frame(self.center_frame, bg=self.dataGui["bg"], height=200)
        self.center_log_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.center_log_frame.pack_propagate(False)

        self.right_frame = tk.Frame(self.game_frame, width=400, height=700, bg=self.dataGui["bg"])
        self.right_frame.pack(side="left", fill="y", padx=5, pady=5)
        self.right_frame.pack_propagate(False)

        self.create_start_action_buttons()
        self.create_event_log()

    def clear_frame(self, frame):
        if frame and frame.winfo_exists():
            children = frame.winfo_children()
            if not children:
                return 
            for widget in children:
                widget.destroy()

    def enemy_info(self, enemy):
        enemy_info_ = f"""Enemy: {enemy.name}
            HP: {enemy.hp}
            Attack: {enemy.attack}
            Defense: {enemy.defense}
            EXP Reward: {enemy.exp}
            Description: {enemy.description}"""
        self._create_info_card(self.left_frame, enemy_info_, "lightgray")

    def npc_info(self, npc):
        npc_info_ = f"""NPC: {npc.name}
            Role: {npc.role}
            Description: {npc.description}
            Services: {", ".join(npc.services)}
            Location: {npc.location}"""
        self._create_info_card(self.left_frame, npc_info_, "lightgray")

    def player_info(self, player):
        player_info_ = f"""Name: {player.name}
            Class: {player.class_name}
            HP: {player.hp}
            SP: {player.sp}
            Attack: {player.attack}
            Defence: {player.defense}"""
        self._create_info_card(self.right_frame, player_info_, "lightblue")

    def _create_info_card(self, parent, text, bg_color):
        card = tk.Frame(parent, bg=bg_color, bd=2, relief="ridge")
        card.pack(pady=15, padx=10, fill="x")

        label = tk.Label(card, text=text, font=("Arial", 12), justify="left",
                         anchor="nw", bg=bg_color, wraplength=370, padx=8, pady=8)
        label.pack(fill="both", expand=True)

    def _create_hover_button(self, parent, text, command, bg, hover_bg):
        btn = tk.Button(parent, text=text, width=20, height=2,
                        bg=bg, activebackground=hover_bg,
                        relief="raised", font=("Arial", 11), command=command)

        def on_enter(e): btn.config(bg=hover_bg)
        def on_leave(e): btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.pack(pady=5)
        return btn

    def create_npc_action_buttons(self, npc):
        self.clear_frame(self.center_buttons_frame)
        for service in npc.services:
            self._create_hover_button(self.center_buttons_frame, service.capitalize(),
                                      lambda s=service: self.controller.npc_action(npc, s),
                                      bg="#d9d9d9", hover_bg="#c0c0c0")

        self._create_hover_button(self.center_buttons_frame, "Leave",
                                  self.controller.current_zon,
                                  bg="#ffcccc", hover_bg="#ff9999")

    def create_start_action_buttons(self):
        self.clear_frame(self.center_buttons_frame)
        buttons_info = [
            ("Castle", self.controller.go_to_castle),
            ("Gateway", self.controller.go_to_gate),
            ("Forest", self.controller.go_to_forest)
        ]
        for text, command in buttons_info:
            self._create_hover_button(self.center_buttons_frame, text, command,
                                      bg="#d9d9d9", hover_bg="#c0c0c0")

    def create_battle_action_buttons(self):
        self.clear_frame(self.center_buttons_frame)
        buttons_info = [
            ("Attack", self.controller.attack_action),
            ("Defend", self.controller.defend_action),
            ("Run", self.controller.run_action)
        ]
        for text, command in buttons_info:
            self._create_hover_button(self.center_buttons_frame, text, command,
                                      bg="#ffdddd", hover_bg="#ffbbbb")

    def create_return_home_button(self, command, enabled):
        self.clear_frame(self.center_buttons_frame)

        state = "normal" if enabled else "disabled"
        btn = tk.Button(self.center_buttons_frame, text="Return Home", width=20, height=2,
                        state=state, bg="#ccffcc", activebackground="#99ff99",
                        relief="raised", font=("Arial", 11), command=command)

        btn.pack(pady=5)

    def create_castle_screen(self, event):
        pass

    def create_forest_screen(self):
        pass

    def create_gate_screen(self):
        pass