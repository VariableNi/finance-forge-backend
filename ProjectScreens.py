import customtkinter as ctk
import requests

API_URL = "http://127.0.0.1:8000"

class ProjectFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.projects_map = {}
        self.goals_map = {}
        
        self.combo_projects = ctk.CTkComboBox(self, values=["Загрузка..."], width=250, font=("Arial", 15, "bold"), command=self.refresh_goals)
        self.combo_projects.pack(pady=10)
        
        self.combo_goals = ctk.CTkComboBox(self, values=["Загрузка..."], width=250, font=("Arial", 15, "bold"))
        self.combo_goals.pack(pady=15)
        
        self.refresh_projects()
    
    def refresh_goals(self, choice):
        try:
            project_id = self.projects_map.get(choice)
            response = requests.get(API_URL+"/projects/"+str(project_id)+"/goals/")
            if response.status_code == 200:
                goals_list = response.json()
                
                if not goals_list:
                    self.combo_goals.configure(values=["Нет активных целей"])
                    return

                # Собираем словарь {"Название": id}
                self.goals_map = {g["title"]: g["id"] for g in goals_list}
                
                # Обновляем выпадающий список
                titles = list(self.goals_map.keys())
                self.combo_goals.configure(values=titles)
                self.combo_goals.set(titles[0]) # Ставим первую цель по умолчанию
            
            else:
                print(response.status_code)

        except requests.exceptions.ConnectionError:
            pass

    def refresh_projects(self):
        try:
            response = requests.get(API_URL+"/projects/")
            if response.status_code == 200:
                projects_list = response.json()
                
                if not projects_list:
                    self.combo_projects.configure(values=["Нет активных целей"])
                    return

                # Собираем словарь {"Название": id}
                self.projects_map = {p["title"]: p["id"] for p in projects_list}
                
                # Обновляем выпадающий список
                titles = list(self.projects_map.keys())
                self.combo_projects.configure(values=titles)
                self.combo_projects.set(titles[0]) # Ставим первую цель по умолчанию
                
            else:
                pass
        except requests.exceptions.ConnectionError:
            pass
        