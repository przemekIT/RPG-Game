import tkinter as tk

class InventoryGUI:
    def __init__(self, root, data_items):
        self.root = root

        self.inventory_frame = tk.Frame(root, bg="lightgray", bd=2, relief="groove")
        self.inventory_frame.pack(side="bottom", fill="x", padx=5, pady=5)
        
        self.create_inventory()
    

    # def create_inventory(self):
    #     self.item_buttons = []
    #     for i in range(10):
    #         cell_frame = tk.Frame(self.inventory_frame, bg="lightblue", width=50, height=50)
    #         cell_frame.grid(row=0, column=i, padx=5, pady=5)

    #         if i < len(self.items):
    #             item = self.items[i]
    #             item_button = tk.Button(cell_frame, text=item['name'], width=8, height=2, command=lambda idx=i: self.use_item(idx))
    #             item_button.pack(expand=True)

    #             self.item_buttons.append(item_button)
    #             empty_label = tk.Label(cell_frame, text="Empty", bg="lightgray", width=8, height=2)
    #             empty_label.pack(expand=True)
    #             self.item_buttons.append(empty_label)
    
    # def use_item(self, index):
    #     item = self.items[index]
    #     print(f"Using item: {item['name']}")
    #     self.show_item_info(item)

    # def show_item_info(self, item):
    #     print(f"Item Info: {item['description']}")
    #     item_info_label = tk.Label(self.root, text=f"Info: {item['description']}", bg="white", font=("Arial", 12))
    #     item_info_label.pack(side="bottom", fill="x", pady=5)