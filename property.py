from tkinter import *
from tkinter import messagebox,ttk

class Property:
    def __init__(self, window, canvas, frame_canvas, old_frame):
        self.window = window
        self.canvas = canvas
        self.frame_canvas = frame_canvas
        self.old_frame = old_frame
        self.frame = Frame(window, bg="#273C28", highlightthickness=5, pady=10, padx=2, highlightbackground="grey")
        self.frame_structure()

    def frame_structure(self):
        Label(self.frame, text="Property", bg="#273C28", borderwidth=5, font=("Georgia", 30, "bold italic"), fg="#fff").grid(row=0, column=0, columnspan=2, pady=(20,20), padx=20)
        self.canvas.coords(self.frame_canvas, 130, 80)
        self.radio_value = StringVar()
        Radiobutton(self.frame, text="Add", variable=self.radio_value, value="1", bg="#273C28", fg="#fff", command=self.add_property, font= ("Courier", 18, "normal")).grid(row=1,column=0, pady=(2, 10), padx=(100, 50),columnspan=1,)
        Radiobutton(self.frame, text="Remove", variable=self.radio_value, value="2", bg="#273C28", fg="#fff", command=self.remove_property, font= ("Courier", 18, "normal")).grid(row=1, column=1, pady=(2, 10), padx=(50, 100),columnspan=1,)

    def add_property(self):
        pass

    def remove_property(self):
        self.canvas.coords(self.frame_canvas, 110, 80)
        ids = ["1", "2", "3"]

        Label(self.frame, text="Select Property:", fg="#fff", bg="#273C28", font=("Courier", 18, "bold")).grid(row=2, column=0,padx=(0,30),columnspan=2,pady=(30,5))
        deactivation_id = StringVar()
        ttk.Combobox(self.frame, textvariable=deactivation_id, width=20, values=ids).grid(row=3, column=0, pady=(5, 20), padx=(10, 10),columnspan=2)

        Button(self.frame, text="Remove", highlightthickness=0, width=10, height=2,
                                         highlightbackground="#273C28", font=("Courier", 15, "bold"),).grid(row=4, column=0, pady=(10,10), padx=30, columnspan=2)
        Button(self.frame, text=" 🔙 ", highlightthickness=0, width=2, height=2, highlightbackground="#273C28", font=("Courier", 15, "bold"), command=self.on_back_click).grid(row=5, column=1, pady=(0, 5), columnspan=1,padx=(200,20))

    def on_back_click(self):
        self.canvas.itemconfig(self.frame_canvas, window=self.old_frame, anchor="nw", )
        self.canvas.coords(self.frame_canvas, 200, 80)
