import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
from datetime import datetime
from tkcalendar import DateEntry
from datetime import date

from fileHelper import CONFIG_PATH, get_data_folder

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.data_folder_path = ctk.StringVar(value=get_data_folder())
        
        # --- CHOIX DU DOSSIER DATA ---
        ctk.CTkLabel(self, text="Dossier de stockage des données :", anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(fill="x", padx=20)
        
        self.folder_entry = ctk.CTkEntry(folder_frame, textvariable=self.data_folder_path)
        self.folder_entry.pack(side="left", fill="x", expand=True, pady=5)
        
        browse_btn = ctk.CTkButton(folder_frame, text="Parcourir", width=100, command=self.browse_folder)
        browse_btn.pack(side="left", padx=10, pady=5)

        # --- AJOUTER UNE LIGNE OPALE ---
        ctk.CTkLabel(self, text="Ajouter une ligne Opale :", anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        opale_frame = ctk.CTkFrame(self)
        opale_frame.pack(fill="x", padx=20)

        self.opale_title_var = ctk.StringVar()

        # Plus besoin d'entrée ID, juste titre
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
            # Créer le dossier s'il n'existe pas
            os.makedirs(folder_selected, exist_ok=True)

            # Créer opale.json vide si inexistant
            opale_path = os.path.join(folder_selected, "opale.json")
            if not os.path.exists(opale_path):
                with open(opale_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2, ensure_ascii=False)

            # Créer tasks.json vide si inexistant
            tasks_path = os.path.join(folder_selected, "tasks.json")
            if not os.path.exists(tasks_path):
                with open(tasks_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2, ensure_ascii=False)

            # Mettre à jour le champ et le fichier config.json
            self.data_folder_path.set(folder_selected)
            config = {}

            if os.path.exists(CONFIG_PATH):
                try:
                    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        config = json.load(f)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de lire config.json : {e}")
                    return

            config["data_folder"] = folder_selected
            try:
                with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Info", "Chemin du dossier data mis à jour et fichiers créés si besoin.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder config.json : {e}")

    def add_opale(self):
        opale_title = self.opale_title_var.get().strip()
        if not opale_title:
            messagebox.showerror("Erreur", "Le titre ne peut pas être vide.")
            return

        opale_path = os.path.join(get_data_folder(), "opale.json")
        try:
            if os.path.exists(opale_path):
                with open(opale_path, "r", encoding="utf-8") as f:
                    opale_list = json.load(f)
            else:
                opale_list = []

            # Générer un nouvel ID unique (max ID + 1)
            if opale_list:
                max_id = max(item["id"] for item in opale_list)
                new_id = max_id + 1
            else:
                new_id = 1

            opale_list.append({"id": new_id, "title": opale_title})

            with open(opale_path, "w", encoding="utf-8") as f:
                json.dump(opale_list, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Succès", f"Ligne Opale ajoutée avec succès")
            self.opale_title_var.set("")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")


    def delete_tasks(self):
        start_str = self.del_start_date.get()  # ex: '2025-07-02'
        end_str = self.del_end_date.get()

        # Pour avoir un datetime ISO complet, on ajoute heure/minute si tu veux :
        start_date = datetime.fromisoformat(start_str + "T00:00:00")
        end_date = datetime.fromisoformat(end_str + "T23:59:59")

        if start_date > end_date:
            messagebox.showerror("Erreur", "La date de début doit être avant la date de fin.")
            return

        try:
            start_date = datetime.fromisoformat(start_str)
            end_date = datetime.fromisoformat(end_str)
        except ValueError:
            messagebox.showerror("Erreur", "Dates invalides. Utilisez le format ISO (ex: 2025-07-01T10:00:00).")
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

        # Reset champs
        self.del_start_date.set_date(date.today())
        self.del_end_date.set_date(date.today())
