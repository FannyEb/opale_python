from PIL import Image
import customtkinter as ctk
from managers.ConfigManager import get_appearance_mode, get_theme_path
from ui.DailyTasksPage import DailyTasksPage
from ui.MonthlySummaryPage import MonthlySummaryPage
from ui.SettingsPage import SettingsPage
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

custom_theme_path = get_theme_path()
custom_appearance_mode = get_appearance_mode()
ctk.set_appearance_mode(custom_appearance_mode)
ctk.set_default_color_theme(custom_theme_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Organisator")
        self.geometry("1000x700")
        self.update_idletasks()

        # Frame de navigation
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(side="top", fill="x")

        title_label = ctk.CTkLabel(nav_frame, text="OPALE", font=("Arial", 20, "bold"), cursor="hand2")
        title_label.pack(side="left", padx=20, pady=10)
        title_label.bind("<Button-1>", lambda e: self.show_daily())

        spacer = ctk.CTkLabel(nav_frame, text="")
        spacer.pack(side="left", expand=True)

        btn_monthly = ctk.CTkButton(nav_frame, text="Résumé du mois", command=self.show_monthly, width=120)
        btn_monthly.pack(side="left", padx=10, pady=10)

        gear_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/setting.png")),
            dark_image=Image.open(resource_path("assets/setting.png")),
            size=(20, 20)
        )
        btn_settings = ctk.CTkButton(nav_frame, text="", image=gear_image, width=40, command=self.show_settings)
        btn_settings.pack(side="left", padx=10, pady=10)

        # === Ici : le scroll global ===
        self.scroll_container = ctk.CTkScrollableFrame(self, width=1000, height=700)
        self.scroll_container.pack(fill="both", expand=True, padx=20, pady=10)

        # === Charger les pages dedans ===
        self.frames = {}
        for F in (SettingsPage, DailyTasksPage, MonthlySummaryPage):
            page_name = F.__name__
            frame = F(parent=self.scroll_container, controller=self)
            self.frames[page_name] = frame
            frame.pack(fill="both", expand=True)

        self.show_daily()

    def show_settings(self):
        self.show_frame("SettingsPage")

    def show_daily(self):
        self.show_frame("DailyTasksPage")

    def show_monthly(self):
        self.show_frame("MonthlySummaryPage")

    def show_frame(self, page_name):
        # Cacher toutes les pages
        for f in self.frames.values():
            f.pack_forget()

        # Afficher celle demandée
        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)

        # Optionnel : exécuter logique si nécessaire
        if page_name == "MonthlySummaryPage":
            frame.display_summary()
        elif page_name == "DailyTasksPage":
            frame.display_tasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()
