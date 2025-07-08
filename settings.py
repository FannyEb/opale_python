import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
from datetime import datetime, date
from tkcalendar import DateEntry

# Pour localiser dans un dossier utilisateur stable
import sys
import shutil

from fileHelper import get_data_folder

def resource_path(relative_path):
    """Pour PyInstaller ou normal"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_persistent_data_folder():
    app_dir = os.path.join(os.path.expanduser("~"), ".OPALE")
    os.makedirs(app_dir, exist_ok=True)

    # Si config.json n'existe pas, on copie un config par défaut depuis ressources
    config_path = os.path.join(app_dir, "config.json")
    if not os.path.exists(config_path):
        try:
            default_config = resource_path("data/config.json")
            shutil.copy(default_config, config_path)
        except Exception:
            # ou au moins créer vide
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"data_folder": app_dir}, f, indent=2, ensure_ascii=False)

    # Pareil pour opale.json
    opale_path = os.path.join(app_dir, "opale.json")
    if not os.path.exists(opale_path):
        with open(opale_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    # Pareil pour tasks.json
    tasks_path = os.path.join(app_dir, "tasks.json")
    if not os.path.exists(tasks_path):
        with open(tasks_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    return app_dir

def get_config_path():
    return os.path.join(get_persistent_data_folder(), "config.json")


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

        del_tasks_btn = ctk.CTkButton(self, text="Supprimer tâches", fg_color="#d9534f", hover_color="#c9302c", command=self.delete_tasks)
        del_tasks_btn.pack(pady=15)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            os.makedirs(folder_selected, exist_ok=True)

            # Créer les fichiers si nécessaires
            for name in ["opale.json", "tasks.json"]:
                path = os.path.join(folder_selected, name)
                if not os.path.exists(path):
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump([], f, indent=2, ensure_ascii=False)

            # Mettre à jour config.json
            self.data_folder_path.set(folder_selected)
            config_path = get_config_path()
            config = {"data_folder": folder_selected}
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Info", "Chemin du dossier data mis à jour et fichiers créés si besoin.")

    def add_opale(self):
        opale_title = self.opale_title_var.get().strip()
        if not opale_title:
            messagebox.showerror("Erreur", "Le titre ne peut pas être vide.")
            return

        opale_path = os.path.join(get_data_folder(), "opale.json")
        try:
            with open(opale_path, "r", encoding="utf-8") as f:
                opale_list = json.load(f)
        except FileNotFoundError:
            opale_list = []

        new_id = max([item["id"] for item in opale_list], default=0) + 1
        opale_list.append({"id": new_id, "title": opale_title})

        with open(opale_path, "w", encoding="utf-8") as f:
            json.dump(opale_list, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("Succès", f"Ligne Opale ajoutée avec succès")
        self.opale_title_var.set("")

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

        tasks_path = os.path.join(get_data_folder(), "tasks.json")
        try:
            with open(tasks_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning("Avertissement", "Fichier tasks.json introuvable.")
            return

        filtered_tasks = [
            t for t in tasks
            if not (t.get("date") and start_date <= datetime.fromisoformat(t["date"].replace("Z", "+00:00")) <= end_date)
        ]

        deleted_count = len(tasks) - len(filtered_tasks)
        with open(tasks_path, "w", encoding="utf-8") as f:
            json.dump(filtered_tasks, f, indent=2, ensure_ascii=False)

        messagebox.showinfo("Info", f"{deleted_count} tâche(s) supprimée(s).")
        self.del_start_date.set_date(date.today())
        self.del_end_date.set_date(date.today())
