import customtkinter as ctk
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Forge(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Forge")
        self.geometry("450x450")
        # self.resizable(False, False)

        self.goals_map = {}

        # interface

        self.title = ctk.CTkLabel(master=self, text="Forge", font=("Arial", 20, "bold"))
        self.title.pack(pady=10, expand=True)

        self.entry = ctk.CTkEntry(master=self, placeholder_text="Enter...", font=("Arial", 20, "bold"))
        self.entry.pack(pady=10, expand=True)
        

if __name__ == "__main__":
    app = Forge()
    app.mainloop()  