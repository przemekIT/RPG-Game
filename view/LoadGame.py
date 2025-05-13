import tkinter as tk
from typing import Callable, Optional, Any, Union

class LoadGame:
    def __init__(self, parent: tk.Widget, saves_list: list[tuple[str, Optional[dict[str, Any]]]],
            select_callback: Callable[[str], None], back_callback: Callable[[], None]) -> None:
        self.parent = parent
        self.saves_list = saves_list
        self.select_callback = select_callback
        self.back_callback = back_callback

        self.create_load_screen()

    def create_load_screen(self) -> None:
        frame = tk.Frame(self.parent, bg=self.parent["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(frame, text="Load Game", font=("Arial", 24), bg=self.parent["bg"], fg="white")
        label.pack(pady=(0, 30))

        for slot, save_entry in self.saves_list:
            self._create_save_button(frame, slot, save_entry)

        back_btn = tk.Button(frame, text="Back", width=20, height=2,
                             bg="#cccccc", activebackground="#aaaaaa",
                             relief="raised", font=("Arial", 11),
                             command=self.back_callback)
        back_btn.pack(pady=(40, 0))

    def _create_save_button(self, parent: Union[tk.Frame, tk.Tk, tk.Toplevel], slot: str, save_entry: Optional[dict[str, Any]]) -> None:
        if save_entry is None:
            text = f"{slot} - Empty"
            state = "disabled"
            command = None
            bg = "#555555"  
            hover_bg = "#555555"
            fg = "#dddddd" 
        else:
            player_name = save_entry["name"]
            text = f"{slot} - {player_name}"
            state = "normal"
            command = lambda s=slot: self.select_callback(s)
            bg = "#447744"    
            hover_bg = "#559955"    
            fg = "#ffffff"       

        btn = tk.Button(parent, text=text, width=20, height=2,
                        state=state, bg=bg, activebackground=hover_bg,
                        fg=fg, activeforeground="#ffffff",
                        relief="raised", font=("Arial", 11, "bold"), command=command)

        def on_enter(e: Any) -> None:
            if state == "normal":
                btn.config(bg=hover_bg)

        def on_leave(e: Any) -> None:
            btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.pack(pady=10)
