import customtkinter as ctk
import requests
from ProjectScreens import ProjectFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

API_URL = "http://127.0.0.1:8000"

class Forge(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Forge")
        self.geometry("600x700")
        self.attributes("-alpha", 0.8)
        self.MIN_WIDTH = 70 
        self.MAX_WIDTH = 200 
        self.current_width = self.MIN_WIDTH
        self.animation_id = None
        
        self.project_frame = ProjectFrame(master=self)
        
        # sidebar------------------------------------------------------------------------------------------
        
        # sidebar with button for open any frame 
        self.sidebar = ctk.CTkFrame(self, width=self.current_width, corner_radius=0, fg_color="#45adff")
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False) 
        self.sidebar.bind("<Enter>", self.on_enter)
        self.sidebar.bind("<Leave>", self.on_leave)
        
        # button of sidebar
        self.project_frame_btn = ctk.CTkButton(master=self.sidebar, text="PF", command=self.open_project_frame)
        self.project_frame_btn.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)
        
        #--------------------------------------------------------------------------------------------------
        
        
    def open_project_frame(self):
         self.project_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)  
    
    def on_enter(self, event):
        """Когда мышь зашла на панель"""
        if self.animation_id:
            self.after_cancel(self.animation_id) # Останавливаем закрытие, если оно шло
        self.animate_expand()

    def on_leave(self, event):
        """Когда мышь ушла с панели"""
        # Проверяем, что мышь действительно ушла СОВСЕМ за пределы панели, 
        # а не просто переключилась на кнопку внутри нее
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        if widget not in [self.sidebar, self.btn1, self.btn2]:
            if self.animation_id:
                self.after_cancel(self.animation_id)
            self.animate_collapse() 
        
        
        # self.configure(fg_color="#0A0A0A")
        # self.resizable(False, False)
        
#         self.combo_projects.configure(
#     fg_color="#2B2B2B",          # Цвет самого поля
#     border_color="#3E3E3E",      # Цвет рамки
#     button_color="#3E3E3E",      # Цвет стрелочки
#     button_hover_color="#5A5A5A",# Цвет стрелочки при наведении
#     dropdown_fg_color="#2B2B2B", # Цвет выпадающего меню
#     dropdown_hover_color="#1F1F1F", # Цвет при наведении на элемент в списке
#     dropdown_text_color="#FFFFFF" # Цвет текста в списке
# )
        
if __name__ == "__main__":
    app = Forge()
    app.mainloop()  
    