import tkinter as tk
from tkinter import ttk 

class CreateGame:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        self.create_character_screen()

    def create_character_screen(self):
        frame = tk.Frame(self.parent, bg=self.parent["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(frame, text="New Game", font=("Arial", 24), bg=self.parent["bg"])
        label.pack(pady=(0, 30))

        name_frame = tk.Frame(frame, bg=self.parent["bg"])
        name_frame.pack(pady=(20, 10))

        name_label = tk.Label(name_frame, text="Name:", bg=self.parent["bg"])
        name_label.pack(side="left", padx=5)

        # Виправлено self.parent замість self.roparentt
        self.name_entry = tk.Entry(name_frame, bg="white")
        self.name_entry.config(width=20)
        self.name_entry.pack(side="right", padx=5)

        class_frame = tk.Frame(frame, bg=self.parent["bg"])
        class_frame.pack(pady=10)

        class_label = tk.Label(class_frame, text="Class", bg=self.parent["bg"])
        class_label.pack(side="left", padx=5)

        self.classes = tk.StringVar()
        self.classes.set("Warrior")

        class_menu = ttk.Combobox(class_frame, textvariable=self.classes, values=["Warrior", "Mage"])
        class_menu.set("Warrior")
        class_menu.config(width=20, state="readonly")
        class_menu.pack(side="left", padx=5)

        create_btn = tk.Button(frame, text="Create", command=self.confirm_creation)
        create_btn.pack(pady=(30, 0))


    def confirm_creation(self):
        name = self.name_entry.get()
        char_class = self.classes.get()
        self.controller.create_character(name, char_class)