import tkinter as tk
from tkinter import Frame, Label, Button, Text, Scrollbar, END, LEFT, RIGHT, BOTH, Y


class GameView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Gra RPG")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self._build_main_layout()
        self.create_action_buttons()

    # === Layout ===
    def _build_main_layout(self):
        self.stats_frame = Frame(self.root)
        self.stats_frame.pack(fill="x", pady=5)

        self.stats_label = Label(
            self.stats_frame,
            text="Statystyki gracza",
            anchor="w",
            justify="left",
            font=("Arial", 10),
        )
        self.stats_label.pack(side=LEFT, padx=10)

        self.location_frame = Frame(self.root)
        self.location_frame.pack(fill="x", pady=5)

        self.location_label = Label(
            self.location_frame, text="Lokalizacja: ", font=("Arial", 12, "bold")
        )
        self.location_label.pack()

        self.log_frame = Frame(self.root)
        self.log_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.log_text = Text(
            self.log_frame, wrap="word", height=15, state="disabled", bg="#f0f0f0"
        )
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        self.action_frame = Frame(self.root)
        self.action_frame.pack(pady=10)

        self.battle_frame = Frame(self.root)

    # === Okna startowe i dialogowe ===
    def show_start_screen(self, on_new_game, on_load_game):
        start_window = tk.Toplevel(self.root)
        start_window.title("Witaj w RPG game!")
        start_window.geometry("300x200")
        start_window.resizable(False, False)

        Label(start_window, text="Wybierz opcję:", font=("Arial", 12, "bold")).pack(
            pady=20
        )

        Button(
            start_window,
            text="Nowa Gra",
            width=20,
            command=lambda: [start_window.destroy(), on_new_game()],
        ).pack(pady=5)
        Button(
            start_window,
            text="Wczytaj Grę",
            width=20,
            command=lambda: [start_window.destroy(), on_load_game()],
        ).pack(pady=5)

    def prompt_player_name(self, on_submit):
        name_window = tk.Toplevel(self.root)
        name_window.title("Wpisz imię")
        name_window.geometry("300x150")
        name_window.resizable(False, False)

        Label(name_window, text="Podaj imię swojej postaci:").pack(pady=10)

        name_entry = tk.Entry(name_window, width=30)
        name_entry.pack(pady=5)

        def submit_name():
            name = name_entry.get().strip()
            if name:
                name_window.destroy()
                on_submit(name)

        Button(name_window, text="Rozpocznij grę", command=submit_name).pack(pady=10)

    def show_game_over_screen(self):
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("Game Over")
        game_over_window.geometry("400x200")
        game_over_window.resizable(False, False)

        Label(
            game_over_window, text="GAME OVER", font=("Arial", 20, "bold"), fg="red"
        ).pack(pady=20)
        Label(game_over_window, text="Twoja postać zginęła.", font=("Arial", 12)).pack(
            pady=10
        )

        Button(
            game_over_window,
            text="Zacznij Nową Grę",
            width=20,
            command=lambda: [
                game_over_window.destroy(),
                self.controller.restart_game(),
            ],
        ).pack(pady=10)

    # === Obsługa GUI ===
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)
        self.log_text.config(state="disabled")

    def show_message(self, message):
        self.log(message)

    def display_location(self, location):
        self.location_label.config(text=f"Lokalizacja: {location.name}")
        self.log(f"Jesteś w {location.name}. {location.description}")

    def update_stats(self, player):
        if player.hp < 30:
            fg_color = "red"
        elif player.hp < 70:
            fg_color = "orange"
        else:
            fg_color = "green"

        self.stats_label.config(
            text=f"{player.name} | HP: {player.hp} | EXP: {player.exp} | Poziom: {player.level}",
            fg=fg_color,
        )

    def clear_action_buttons(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

    def clear_battle_frame(self):
        for widget in self.battle_frame.winfo_children():
            widget.destroy()

    # === Interfejs walki ===
    def show_fight_interface(self, enemy):
        self.action_frame.pack_forget()
        self.clear_battle_frame()
        self.battle_frame.pack(pady=10)

        self.enemy_hp_label = Label(
            self.battle_frame,
            text=f"{enemy.name} HP: {enemy.hp}",
            font=("Arial", 12, "bold"),
            fg="red",
        )
        self.enemy_hp_label.pack()

        Button(
            self.battle_frame,
            text="Atakuj",
            width=15,
            command=self.controller.player_attack,
        ).pack(side=LEFT, padx=5)
        Button(
            self.battle_frame,
            text="Użyj ekwipunek",
            width=15,
            command=self.controller.open_inventory,
        ).pack(side=LEFT, padx=5)
        Button(
            self.battle_frame,
            text="Uciekaj",
            width=15,
            command=self.controller.attempt_escape,
        ).pack(side=LEFT, padx=5)

    def update_enemy_hp(self, enemy):
        if hasattr(self, "enemy_hp_label"):
            self.enemy_hp_label.config(text=f"{enemy.name} HP: {enemy.hp}")

    def show_main_menu(self):
        self.battle_frame.pack_forget()
        self.clear_battle_frame()
        self.action_frame.pack(pady=10)
        self.create_action_buttons()

    # === Przyciski akcji ===
    def create_action_buttons(self):
        self.clear_action_buttons()

        Button(
            self.action_frame,
            text="Eksploruj",
            width=15,
            command=self.controller.explore,
        ).pack(side=LEFT, padx=5)
        Button(
            self.action_frame, text="Rozmowa", width=15, command=self.controller.talk
        ).pack(side=LEFT, padx=5)
        Button(
            self.action_frame, text="Walka", width=15, command=self.controller.fight
        ).pack(side=LEFT, padx=5)
        Button(
            self.action_frame,
            text="Zmień Lokację",
            width=15,
            command=self.controller.change_location,
        ).pack(side=LEFT, padx=5)
        Button(
            self.action_frame,
            text="Zapisz grę",
            width=15,
            command=self.controller.save_game,
        ).pack(side=LEFT, padx=5)

    # === Ekwipunek ===
    def show_inventory(self, inventory):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Ekwipunek")
        inventory_window.geometry("300x400")

        Label(
            inventory_window, text="Twój ekwipunek:", font=("Arial", 12, "bold")
        ).pack(pady=10)

        if not inventory:
            Label(inventory_window, text="Ekwipunek jest pusty.").pack(pady=10)
        else:
            for item in inventory:
                item_frame = Frame(inventory_window)
                item_frame.pack(pady=5)

                Label(item_frame, text=item.name).pack(side=LEFT, padx=5)
                Button(
                    item_frame,
                    text="Użyj",
                    command=lambda i=item, w=inventory_window: self.use_and_close(i, w),
                ).pack(side=RIGHT, padx=5)

        Button(inventory_window, text="Zamknij", command=inventory_window.destroy).pack(
            pady=10
        )

    def use_and_close(self, item, window):
        self.controller.use_item(item)
        window.destroy()

    # === NPC ===
    def show_npc_dialogue(self, npc):
        dialogue_window = tk.Toplevel(self.root)
        dialogue_window.title(f"Rozmowa z {npc.name}")
        dialogue_window.geometry("400x300")

        Label(
            dialogue_window, text=f"Rozmawiasz z {npc.name}", font=("Arial", 12, "bold")
        ).pack(pady=10)

        response_text = Text(dialogue_window, wrap="word", height=6, state="disabled")
        response_text.pack(fill=BOTH, expand=True, padx=10, pady=10)

        def handle_choice(question):
            response = npc.respond_to(question)
            item = npc.give_item()
            if item:
                self.controller.player.inventory.append(item)
                response += f"\n\n{npc.name} daje Ci przedmiot: {item.name}!"
            response_text.config(state="normal")
            response_text.delete("1.0", END)
            response_text.insert(END, response)
            response_text.config(state="disabled")

        for question in npc.get_dialogue_options():
            Button(
                dialogue_window,
                text=question,
                command=lambda q=question: handle_choice(q),
            ).pack(pady=2)

        Button(dialogue_window, text="Zakończ", command=dialogue_window.destroy).pack(
            pady=10
        )


    def show_game_win_screen(self):
        win_window = tk.Toplevel(self.root)
        win_window.title("Wygrana!")
        win_window.geometry("400x200")
        win_window.resizable(False, False)

        Label(
            win_window, text="WYGRAŁEŚ!", font=("Arial", 20, "bold"), fg="green"
            ).pack(pady=20)
        Label(win_window, text="Gratulacje, osiągnąłeś maksymalny poziom!", font=("Arial", 12)).pack(pady=10)

        Button(
            win_window,
            text="Zagraj ponownie",
            width=20,
            command=lambda: [
            win_window.destroy(),
            self.controller.restart_game(),
            ],
            ).pack(pady=10)