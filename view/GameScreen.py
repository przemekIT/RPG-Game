import tkinter as tk
from typing import Any, Callable, Optional, Union

class GameScreen:
    def __init__(self, root: tk.Tk, controller: Any, dataGui: dict[str, Any]) -> None:
        self.root = root
        self.controller = controller
        self.event_log: Optional[tk.Text] = None
        self.dataGui = dataGui.get("Window")
        self.player = controller.player

        self.create_screen()
        
    def create_event_log(self) -> None:
        log_border = tk.Frame(self.center_log_frame, bg="#d4c4a8", bd=3, relief="ridge")
        log_border.pack(fill="both", expand=True, padx=5, pady=5)

        self.event_log = tk.Text(
            log_border,
            height=10,
            state="disabled",
            wrap="word",
            bg="#f4ecd8", 
            fg="#4b3f2f", 
            relief="flat",
            bd=0,
            font=("Georgia", 11),
            padx=8,
            pady=8
        )
        self.event_log.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(log_border, command=self.event_log.yview, bg="#c8b894",
                                troughcolor="#e0d2b6", activebackground="#a89b7f",
                                relief="flat", bd=1)
        scrollbar.pack(side="right", fill="y")
        self.event_log.config(yscrollcommand=scrollbar.set)

    def create_screen(self) -> None:
        self.game_frame = tk.Frame(self.root, bg=self.dataGui["bg"])
        self.game_frame.pack(fill="both", expand=True)

        self.inventory_frame = tk.Frame(self.game_frame, bg=self.dataGui["bg"], height=60,)
        self.inventory_frame.pack(side="bottom", fill="x")
        self.inventory_frame.pack_propagate(False)

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
        self.inventory_bar()

    def clear_frame(self, frame: Any) -> None:
        if frame and frame.winfo_exists():
            children = frame.winfo_children()
            if not children:
                return 
            for widget in children:
                widget.destroy()

    def enemy_info(self, enemy: Any) -> None:
        enemy_info_ = f"""Enemy: {enemy.name}
            HP: {enemy.hp}
            Attack: {enemy.attack}
            Defense: {enemy.defense}
            EXP Reward: {enemy.exp}
            Description: {enemy.description}"""
        self._create_info_card(self.left_frame, enemy_info_, "lightgray")

    def npc_info(self, npc: Any) -> None:
        npc_info_ = f"""NPC: {npc.name}
            Role: {npc.role}
            Description: {npc.description}
            Services: {", ".join(npc.services)}
            Location: {npc.location}"""
        self._create_info_card(self.left_frame, npc_info_, "lightgray")

    def player_info(self, player: Any) -> None:
        player_info_ = f"""Name: {player.name}
            Class: {player.class_name}
            HP: {player.hp}
            SP: {player.sp}
            Attack: {player.attack}
            Defence: {player.defense},
            Gold: {player.gold}"""
        self._create_info_card(self.right_frame, player_info_, "lightblue")

    def update_player_info(self) -> None:
        self.player_info(self.controller.player)

    def _create_info_card(self, parent: tk.Widget, text: str, bg_color: str = "#f4ecd8") -> None:
        card = tk.Frame(parent, bg=bg_color, bd=2, relief="ridge")
        card.pack(pady=15, padx=10, fill="x")

        label = tk.Label(
            card,
            text=text,
            font=("Georgia", 11),
            justify="left",
            anchor="nw",
            bg=bg_color,
            fg="#4b3f2f",
            wraplength=370,
            padx=8,
            pady=8
        )
        label.pack(fill="both", expand=True)

    def _create_hover_button(self, parent: tk.Widget, text: str, command: Callable[[], None], bg: str = "#4b3f2f",
            hover_bg: str = "#6a5b45", fg: str = "#f0e6d6") -> tk.Button:
        btn = tk.Button(parent, text=text, width=20, height=2,
                        bg=bg, fg=fg,
                        activebackground=hover_bg, activeforeground="#ffffff",
                        relief="raised", font=("Georgia", 12, "bold"), command=command)

        def on_enter(e): btn.config(bg=hover_bg)
        def on_leave(e): btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.pack(pady=5)
        return btn

    def create_npc_action_buttons(self, npc: Any) -> None:
        for service in npc.services:
            self._create_hover_button(self.center_buttons_frame, service.capitalize(),
                lambda s=service: self.controller.npc_action(npc, s))

        self._create_hover_button(self.center_buttons_frame, "Sell Items",
            lambda: self.controller.npc_action(npc, "Sell Items"))

        self._create_hover_button(self.center_buttons_frame, "Leave",
            self.controller.current_zon, bg="#773333", hover_bg="#992222")

    def create_save_game_buttons(self, load_list: list[tuple[str, Optional[dict[str, Any]]]]) -> None:
        for index, (slot, save_entry) in enumerate(load_list, start=1):
            if save_entry is None:
                text = f"Save Slot {index} - Empty"
                state = "normal"
                command = lambda s=slot: self.controller.saveing(s)
                bg = "#666666"
                hover_bg = "#888888"
            else:
                player_name = save_entry["name"]
                text = f"Save Slot {index} - {player_name}"
                state = "normal"
                command = lambda s=slot: self.controller.saveing(s)
                bg = "#d9d9d9"
                hover_bg = "#c0c0c0"

            self._create_hover_button(
                self.center_buttons_frame, 
                text, 
                command, 
                bg=bg, 
                hover_bg=hover_bg
            )

    def create_start_action_buttons(self) -> None:
        buttons_info = [
            ("Castle", self.controller.go_to_castle),
            ("Gateway", self.controller.go_to_gate),
            ("Forest", self.controller.go_to_forest)
        ]
        for text, command in buttons_info:
            self._create_hover_button(self.center_buttons_frame, text, command)

    def create_battle_action_buttons(self) -> None:
        buttons_info = [
            ("Attack", self.controller.attack_action),
            ("Defend", self.controller.defend_action),
            ("Run", self.controller.run_action)
        ]
        for text, command in buttons_info:
            self._create_hover_button(self.center_buttons_frame, text, command, bg="#773333", hover_bg="#992222")

    def create_return_home_and_save_buttons( self, return_command: Callable[[], None], save_command: Callable[[], None],
            return_enabled: bool, save_enabled: bool) -> None:
        return_state = "normal" if return_enabled else "disabled"
        save_state = "normal" if save_enabled else "disabled"

        btn_home = tk.Button(self.center_buttons_frame, text="Return Home", width=20, height=2,
                            state=return_state,
                            bg="#336633", fg="#f0e6d6",
                            activebackground="#449944", activeforeground="#ffffff",
                            relief="raised", font=("Georgia", 12, "bold"), command=return_command)
        btn_home.pack(pady=5)

        btn_save = tk.Button(self.center_buttons_frame, text="Save Game", width=20, height=2,
                            state=save_state,
                            bg="#663366", fg="#f0e6d6",
                            activebackground="#994499", activeforeground="#ffffff",
                            relief="raised", font=("Georgia", 12, "bold"), command=save_command)
        btn_save.pack(pady=5)

    def show_inventory_actions(self, item: Any, index: int) -> None:
        actions = [
            ("Use", lambda: self.controller.use_item(item)),
            ("Drop", lambda: self.controller.drop_item(index)),
            ("Leave", self.controller.go_back)
        ]
        for text, cmd in actions:
            self._create_hover_button(self.center_buttons_frame, text, cmd)

    def show_inventory(self) -> None:
        for index, item in enumerate(self.inventory_items):
            button = tk.Button(self.center_buttons_frame, text=item.get_item(),
                            command=lambda i=item, idx=index: self.controller.inventory_actions(i, idx),
                            bg="#4b3f2f", fg="#f0e6d6",
                            activebackground="#6a5b45", activeforeground="#ffffff",
                            relief="raised", font=("Georgia", 11), width=20, height=2)
            button.pack(pady=5)

    def show_inventory_info(self, item: Any) -> None:
        if hasattr(self, 'item_info_label'):
            self.item_info_label.destroy()

        self.item_info_label = tk.Label(
            self.game_frame,
            text=f"Item: {item.get_item()}\nDescription: {item.get_description()}",
            font=("Georgia", 12),
            bg=self.dataGui["bg"],
            fg="#f0e6d6",
            padx=10, pady=10,
            justify="left",
            anchor="nw"
        )
        self.item_info_label.pack(pady=10, side="top")

    def show_item_info(self, item: Any) -> None:
        item_info_ = f"""Item: {item.get_item()}
            Description: {item.get_description()}
            {item.get_stat_text()}"""
        self._create_info_card(self.left_frame, item_info_, "lightgray")

    def inventory_bar(self) -> None:
        buttons_container = tk.Frame(self.inventory_frame, bg="#4b3f2f")
        buttons_container.pack(side="top")

        for i in range(10):
            btn = tk.Button(buttons_container, text="Empty", width=8, height=2,
                            bg="#6a5b45", fg="#f0e6d6",
                            activebackground="#8c7b68", activeforeground="#ffffff",
                            relief="raised", font=("Georgia", 10, "bold"),
                            command=lambda idx=i: self.controller.on_inventory_click(idx))
            btn.pack(side="left", padx=2, pady=2)
            self.controller.create_inventory_bar(btn)

        self.controller.update_inventory_bar(self.controller.player.get_inventory())

    def update_event_log(self, message: str) -> None:
        self.event_log.config(state="normal")
        self.event_log.insert("end", message + "\n")
        self.event_log.see("end")
        self.event_log.config(state="disabled")

    def create_castle_screen(self, event):
        pass

    def create_forest_screen(self):
        pass

    def create_gate_screen(self):
        pass