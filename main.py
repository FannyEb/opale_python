from PIL import Image
import customtkinter as ctk
from ui.DailyTasksPage import DailyTasksPage
from ui.MonthlySummaryPage import MonthlySummaryPage
from ui.SettingsPage import SettingsPage
import sys
import os

def resource_path(relative_path):
    """ Obtenir le chemin absolu au fichier, que ce soit dans PyInstaller ou non """
    try:
        # PyInstaller crée un dossier temporaire dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

custom_theme_path = resource_path("style/custom_theme.json")
ctk.set_appearance_mode("System")  # "Dark" ou "System"
ctk.set_default_color_theme(custom_theme_path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Organisator")
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # Frame de navigation (en haut)
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(side="top", fill="x")

        # Label cliquable
        title_label = ctk.CTkLabel(nav_frame, text="OPALE", font=("Arial", 20, "bold"), cursor="hand2")
        title_label.pack(side="left", padx=20, pady=10)
        title_label.bind("<Button-1>", lambda e: self.show_daily())  # clic renvoie aux tâches du jour

        # Spacer
        spacer = ctk.CTkLabel(nav_frame, text="")
        spacer.pack(side="left", expand=True)

        # Bouton résumé du mois
        btn_monthly = ctk.CTkButton(nav_frame, text="Résumé du mois", command=self.show_monthly, width=120)
        btn_monthly.pack(side="left", padx=10, pady=10)

        # Bouton icône settings
        gear_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/setting.png")),
            dark_image=Image.open(resource_path("assets/setting.png")),
            size=(20, 20)
        )
        btn_settings = ctk.CTkButton(nav_frame, text="", image=gear_image, width=40, command=self.show_settings)
        btn_settings.pack(side="left", padx=10, pady=10)

        # Container des pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        # Initialiser les pages
        self.frames = {}
        for F in (SettingsPage, DailyTasksPage, MonthlySummaryPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_daily()  # page initiale

    def show_settings(self):
        self.show_frame("SettingsPage")

    def show_daily(self):
        self.show_frame("DailyTasksPage")

    def show_monthly(self):
        self.show_frame("MonthlySummaryPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "MonthlySummaryPage":
            frame.display_summary()
        elif page_name == "DailyTasksPage":
            frame.display_tasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()
