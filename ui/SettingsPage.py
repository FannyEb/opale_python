import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime, date
from tkcalendar import DateEntry

from managers.OpaleManager import add_opale_line, load_opale_list, delete_opale_line
from managers.TaskManager import delete_tasks_between
from utils.FileUtils import get_data_folder
from ui.Autocomplete import SimpleAutocomplete

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.data_folder_path = ctk.StringVar(value=get_data_folder())

        # --- AJOUTER UNE LIGNE OPALE ---
        ctk.CTkLabel(self, text="Ajouter une ligne Opale :", anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        opale_frame = ctk.CTkFrame(self)
        opale_frame.pack(fill="x", padx=20)

        self.opale_title_var = ctk.StringVar()
        ctk.CTkLabel(opale_frame, text="Titre :", width=40).pack(side="left", padx=5, pady=5)
        opale_title_entry = ctk.CTkEntry(opale_frame, textvariable=self.opale_title_var)
        opale_title_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        add_opale_btn = ctk.CTkButton(self, text="Ajouter Opale", command=self.add_opale)
        add_opale_btn.pack(pady=10)

        # --- SUPPRIMER UNE LIGNE OPALE ---
        ctk.CTkLabel(self, text="Supprimer une ligne Opale :", anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        del_opale_frame = ctk.CTkFrame(self)
        del_opale_frame.pack(fill="x", padx=20)

        opale_titles = [title for _id, title in load_opale_list()]
        self.opale_autocomplete = SimpleAutocomplete(del_opale_frame, opale_titles)
        self.opale_autocomplete.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        del_opale_btn = ctk.CTkButton(del_opale_frame, text="Supprimer", fg_color="#d9534f", hover_color="#c9302c",
                                      command=self.delete_opale)
        del_opale_btn.pack(side="left", padx=5)

        # --- SUPPRIMER LES TACHES ENTRE DEUX DATES ---
        ctk.CTkLabel(self, text="Supprimer tâches entre deux dates :", anchor="w").pack(fill="x", padx=20, pady=(20, 5))

        del_frame = ctk.CTkFrame(self)
        del_frame.pack(fill="x", padx=20)

        ctk.CTkLabel(del_frame, text="Date début :", width=120).pack(side="left", padx=5, pady=5)
        self.del_start_date = DateEntry(del_frame, date_pattern="yyyy-mm-dd")
        self.del_start_date.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(del_frame, text="Date fin :", width=120).pack(side="left", padx=5, pady=5)
        self.del_end_date = DateEntry(del_frame, date_pattern="yyyy-mm-dd")
        self.del_end_date.pack(side="left", padx=5, pady=5)

        del_tasks_btn = ctk.CTkButton(
            self, text="Supprimer tâches", fg_color="#d9534f", hover_color="#c9302c", command=self.delete_tasks
        )
        del_tasks_btn.pack(pady=15)

    def add_opale(self):
        opale_title = self.opale_title_var.get().strip()
        if not opale_title:
            messagebox.showerror("Erreur", "Le titre ne peut pas être vide.")
            return

        add_opale_line(opale_title)
        messagebox.showinfo("Succès", "Ligne Opale ajoutée avec succès")
        self.opale_title_var.set("")
        self.refresh_opale_autocomplete()

    def delete_opale(self):
        selected_title = self.opale_autocomplete.get()
        if not selected_title:
            messagebox.showerror("Erreur", "Veuillez sélectionner une ligne Opale.")
            return

        deleted = delete_opale_line(selected_title)
        if deleted:
            messagebox.showinfo("Succès", f"La ligne Opale '{selected_title}' a été supprimée.")
        else:
            messagebox.showerror("Erreur", f"La ligne Opale '{selected_title}' n'a pas été trouvée.")

        self.refresh_opale_autocomplete()

    def refresh_opale_autocomplete(self):
        opale_titles = [title for _id, title in load_opale_list()]
        self.opale_autocomplete.values = opale_titles
        self.opale_autocomplete.entry.delete(0, ctk.END)
        if self.opale_autocomplete.suggestions_frame:
            self.opale_autocomplete.suggestions_frame.destroy()
            self.opale_autocomplete.suggestions_frame = None

    def delete_tasks(self):
        start_str = self.del_start_date.get()
        end_str = self.del_end_date.get()
        try:
            start_date = datetime.fromisoformat(start_str + "T00:00:00")
            end_date = datetime.fromisoformat(end_str + "T23:59:59")
        except ValueError:
            messagebox.showerror("Erreur", "Dates invalides.")
            return

        if start_date > end_date:
            messagebox.showerror("Erreur", "La date de début doit être avant la date de fin.")
            return

        deleted_count = delete_tasks_between(start_date, end_date)
        messagebox.showinfo("Info", f"{deleted_count} tâche(s) supprimée(s).")

        self.del_start_date.set_date(date.today())
        self.del_end_date.set_date(date.today())
