import tkinter as tk
from tkinter import ttk
from typing import Any

class CreateGame:
    def __init__(self, parent: tk.Widget, controller: Any) -> None:
        self.parent: tk.Widget = parent
        self.controller: Any = controller

        self.create_character_screen()

    def create_character_screen(self) -> None:
        frame = tk.Frame(self.parent, bg=self.parent["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            frame,
            text="New Adventure",
            font=("Georgia", 28, "bold"),
            fg="#f0e6d6",
            bg=self.parent["bg"]
        )
        label.pack(pady=(0, 40))

        name_frame = tk.Frame(frame, bg=self.parent["bg"])
        name_frame.pack(pady=15)

        name_label = tk.Label(
            name_frame,
            text="Name:",
            font=("Georgia", 14),
            fg="#f0e6d6",
            bg=self.parent["bg"]
        )
        name_label.pack(side="left", padx=5)

        self.name_entry = tk.Entry(
            name_frame,
            bg="#e0d4b7",
            fg="#3a2f20",
            insertbackground="#3a2f20",
            font=("Georgia", 12)
        )
        self.name_entry.config(width=24, relief="sunken", bd=2)
        self.name_entry.pack(side="right", padx=5)

        class_frame = tk.Frame(frame, bg=self.parent["bg"])
        class_frame.pack(pady=15)

        class_label = tk.Label(
            class_frame,
            text="Class:",
            font=("Georgia", 14),
            fg="#f0e6d6",
            bg=self.parent["bg"]
        )
        class_label.pack(side="left", padx=5)

        self.classes = tk.StringVar()
        self.classes.set("Warrior")

        class_menu = ttk.Combobox(
            class_frame,
            textvariable=self.classes,
            values=["Warrior", "Mage", "Ranger", "Cleric"]
        )
        class_menu.set("Warrior")
        class_menu.config(width=22, state="readonly")
        class_menu.pack(side="left", padx=5)

        create_btn = tk.Button(
            frame,
            text="Begin Journey",
            command=self.confirm_creation,
            bg="#4b3f2f",
            fg="#f0e6d6",
            activebackground="#6a5b45",
            activeforeground="#ffffff",
            font=("Georgia", 14, "bold"),
            relief="raised",
            bd=3,
            padx=10,
            pady=5
        )
        create_btn.pack(pady=(40, 0))

    def confirm_creation(self) -> None:
        name = self.name_entry.get()
        char_class = self.classes.get()
        self.controller.create_character(name, char_class)
