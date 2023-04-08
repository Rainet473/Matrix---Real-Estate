from tkinter import *
from registration import *


class Agent:
    def __init__(self, window):
        self.frame = Frame(window, bg="#273C28", highlightthickness=5, pady=10, padx=2, highlightbackground="grey")
        self.frame_structure()

    def frame_structure(self):
        self.main_label = Label(self.frame, text="Dashboard", bg="#273C28", borderwidth=5,
                                font=("Georgia", 30, "bold"), fg="#fff")
        self.main_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

        self.assign_button = Button(self.frame, text="Assign", highlightthickness=0, width=15, height=2,
                                    highlightbackground="#273C28", font=("Courier", 20, "bold"), )
        self.assign_button.grid(row=1, column=0, pady=10, padx=10, columnspan=1)
        menu_assign = StringVar()
        menu_assign.set("Select Customer Type")
        self.assign_drop = OptionMenu(self.frame, menu_assign, "Purchaser", "Owner")
        self.assign_drop.grid(row=1, column=1, columnspan=1, pady=10, padx=20)

        self.remove_button = Button(self.frame, text="Remove", highlightthickness=0, width=15, height=2,
                                    highlightbackground="#273C28", font=("Courier", 20, "bold"), )
        self.remove_button.grid(row=2, column=0, pady=10, padx=10, columnspan=1)
        menu_remove = StringVar()
        menu_remove.set("Select Customer Type")
        self.remove_drop = OptionMenu(self.frame, menu_remove, "Purchaser", "Owner")
        self.remove_drop.grid(row=2, column=1, columnspan=1, pady=10, padx=20)

        self.property_button = Button(self.frame, text="Property", highlightthickness=0, width=15, height=2,
                                      highlightbackground="#273C28", font=("Courier", 20, "bold"), )
        self.property_button.grid(row=3, column=0, pady=10, padx=10, columnspan=1)
        menu_property = StringVar()
        menu_property.set("Select dash")
        self.property_drop = OptionMenu(self.frame, menu_property, "Add", "Remove")
        self.property_drop.grid(row=3, column=1, columnspan=1, pady=10, padx=20)

        self.transaction_button = Button(self.frame, text="Transaction", highlightthickness=0, width=15, height=2,
                                         highlightbackground="#273C28", font=("Courier", 20, "bold"), )
        self.transaction_button.grid(row=4, column=0, pady=10, padx=10, columnspan=1)
        menu_transaction = StringVar()
        menu_transaction.set("Select type")
        self.transaction_drop = OptionMenu(self.frame, menu_transaction, "Sale", "Rent")
        self.transaction_drop.grid(row=4, column=1, columnspan=1, pady=10, padx=20)
