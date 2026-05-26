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
        
        self.label_status = ctk.CTkLabel(self, text="Подключение к бэкенду...", text_color="orange")
        self.label_status.pack(pady=(10, 0))
        
        self.combo_goals = ctk.CTkComboBox(self, values=["Загрузка..."], width=250, font=("Arial", 15, "bold"))
        self.combo_goals.pack(pady=10)
        
        self.label_status.bind("<Enter>", self.label_status.configure(text_color="white"))
        self.label_status.bind("<Leave>", self.label_status.configure(text_color="red"))

        # self.title = ctk.CTkLabel(master=self, text="Forge", font=("Arial", 20, "bold"))
        # self.title.pack(pady=10, expand=True)

        # self.entry = ctk.CTkEntry(master=self, placeholder_text="Enter...", font=("Arial", 20, "bold"))
        # self.entry.pack(pady=10, expand=True)
        
        self.refresh_goals()

    def refresh_goals(self):
        """Запрашивает цели с бэкенда FastAPI"""
        try:
            response = requests.get("http://127.0.0.1:8000/goals/")
            if response.status_code == 200:
                goals_list = response.json()
                
                if not goals_list:
                    self.label_status.configure(text="База целей пуста! Добавь их в Swagger.", text_color="yellow")
                    self.combo_goals.configure(values=["Нет активных целей"])
                    return

                # Собираем словарь {"Название": id}
                self.goals_map = {g["title"]: g["id"] for g in goals_list}
                
                # Обновляем выпадающий список
                titles = list(self.goals_map.keys())
                self.combo_goals.configure(values=titles)
                self.combo_goals.set(titles[0]) # Ставим первую цель по умолчанию
                
                self.label_status.configure(text="Молот готов к бою ✅", text_color="green")
            else:
                self.label_status.configure(text=f"Ошибка сервера: {response.status_code}", text_color="red")
        except requests.exceptions.ConnectionError:
            self.label_status.configure(text="Ошибка: Бэкенд не запущен!", text_color="red")
        

if __name__ == "__main__":
    app = Forge()
    app.mainloop()  