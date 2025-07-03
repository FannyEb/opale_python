from PIL import Image
import customtkinter as ctk
from daily_tasks import DailyTasksPage
from monthly_summary import MonthlySummaryPage
from settings import SettingsPage

ctk.set_appearance_mode("Dark")  # "Dark" ou "System"
ctk.set_default_color_theme("./style/custom_theme.json")



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
            light_image=Image.open("assets/icons/setting.png"),
            dark_image=Image.open("assets/icons/setting.png"),
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
        elif page_name == "SettingsPage":
            frame.load_opale_list()

if __name__ == "__main__":
    app = App()
    app.mainloop()
