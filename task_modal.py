import customtkinter as ctk
import json
import os
from datetime import datetime

from fileHelper import get_data_folder

class TaskModal(ctk.CTkToplevel):
    def __init__(self, master, task, json_path, refresh_callback):
        super().__init__(master)

        self.transient(master)   # rattache à la fenêtre principale
        self.grab_set()          # bloque interaction hors modal
        self.focus()             # donne le focus
        self.focus_force()       # force le focus clavier

        self.title("Détails de la tâche")
        self.geometry("400x550")

        self.task = task
        self.json_path = json_path
        self.refresh_callback = refresh_callback

        # Charger la liste Opale
        self.opale_list = self.load_opale_list()

        # ---------------------------
        # TITRE
        # ---------------------------
        title_label = ctk.CTkLabel(self, text="Titre :", anchor="w")
        title_label.pack(fill="x", padx=20, pady=(15, 0))
        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.insert(0, str(task.get("title") or ""))
        self.title_entry.pack(fill="x", padx=20, pady=5)

        # ---------------------------
        # DATE DE DEBUT
        # ---------------------------
        date_label = ctk.CTkLabel(self, text="Date de début (ISO) :", anchor="w")
        date_label.pack(fill="x", padx=20, pady=(15, 0))
        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.insert(0, str(task.get("date") or ""))
        self.date_entry.pack(fill="x", padx=20, pady=5)

        # ---------------------------
        # JIRA
        # ---------------------------
        jira_label = ctk.CTkLabel(self, text="Lien JIRA :", anchor="w")
        jira_label.pack(fill="x", padx=20, pady=(15, 0))
        self.jira_entry = ctk.CTkEntry(self)
        self.jira_entry.insert(0, str(task.get("linkJira") or ""))
        self.jira_entry.pack(fill="x", padx=20, pady=5)

        # ---------------------------
        # SPEC
        # ---------------------------
        spec_label = ctk.CTkLabel(self, text="Lien SPEC :", anchor="w")
        spec_label.pack(fill="x", padx=20, pady=(15, 0))
        self.spec_entry = ctk.CTkEntry(self)
        self.spec_entry.insert(0, str(task.get("linkSpec") or ""))
        self.spec_entry.pack(fill="x", padx=20, pady=5)

        # ---------------------------
        # OPALE (Dropdown)
        # ---------------------------
        opale_label = ctk.CTkLabel(self, text="Opale :", anchor="w")
        opale_label.pack(fill="x", padx=20, pady=(15, 0))

        opale_titles = [title for _id, title in self.opale_list]
        self.opale_var = ctk.StringVar()

        current_id = str(task.get("opale") or "")
        current_title = next((title for _id, title in self.opale_list if _id == current_id), current_id)
        self.opale_var.set(current_title)

        self.opale_menu = ctk.CTkOptionMenu(self, values=opale_titles, variable=self.opale_var)
        self.opale_menu.pack(fill="x", padx=20, pady=5)

        # ---------------------------
        # DATE DE FIN
        # ---------------------------
        end_date_label = ctk.CTkLabel(self, text="Date de fin (ISO) :", anchor="w")
        end_date_label.pack(fill="x", padx=20, pady=(15, 0))
        self.end_date_entry = ctk.CTkEntry(self)
        self.end_date_entry.insert(0, str(task.get("endDate") or ""))
        self.end_date_entry.pack(fill="x", padx=20, pady=5)

        # ---------------------------
        # BOUTON SAUVEGARDER
        # ---------------------------
        save_btn = ctk.CTkButton(self, text="Sauvegarder", command=self.save_task)
        save_btn.pack(pady=20)

    def load_opale_list(self):
        opale_path = os.path.join(get_data_folder(), "opale.json")
        try:
            with open(opale_path, "r", encoding="utf-8") as f:
                opale_list = json.load(f)
            # Retourne liste de tuples (id, titre)
            return [(str(item["id"]), item.get("title", f"Opale {item['id']}")) for item in opale_list]
        except FileNotFoundError:
            return []

    def save_task(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []

        for t in tasks:
            if t["id"] == self.task["id"]:
                t["title"] = self.title_entry.get()
                t["date"] = self.date_entry.get()
                t["linkJira"] = self.jira_entry.get()
                t["linkSpec"] = self.spec_entry.get()

                selected_title = self.opale_var.get()
                selected_id = next((_id for _id, title in self.opale_list if title == selected_title), "0")
                try:
                    t["opale"] = int(selected_id)
                except:
                    t["opale"] = 0

                t["endDate"] = self.end_date_entry.get()
                break

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

        self.refresh_callback()
        self.destroy()
