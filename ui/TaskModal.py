import customtkinter as ctk
from tkinter import messagebox

from managers.OpaleManager import load_opale_list
from managers.TaskManager import load_tasks, save_tasks

class TaskModal(ctk.CTkToplevel):
    def __init__(self, master, task, refresh_callback):
        super().__init__(master)

        self.transient(master)
        self.grab_set()
        self.focus()
        self.focus_force()

        self.title("Détails de la tâche")
        self.geometry("400x600")

        self.task = task
        self.refresh_callback = refresh_callback

        # Chargement Opale
        self.opale_list = load_opale_list()

        # UI
        self.build_ui()

    def build_ui(self):
        self.create_labeled_entry("Titre :", "title", self.task.title)
        self.create_labeled_entry("Date de début (ISO) :", "date", self.task.date)
        self.create_labeled_entry("Lien JIRA :", "linkJira", self.task.linkJira)
        self.create_labeled_entry("Lien SPEC :", "linkSpec", self.task.linkSpec)
        self.create_opale_dropdown()
        self.create_labeled_entry("Date de fin (ISO) :", "endDate", self.task.endDate)

        save_btn = ctk.CTkButton(self, text="Sauvegarder", command=self.save_task)
        save_btn.pack(pady=20)

    def create_labeled_entry(self, label, attr, default_val=""):
        ctk.CTkLabel(self, text=label, anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        entry = ctk.CTkEntry(self)
        entry.insert(0, str(default_val or ""))
        entry.pack(fill="x", padx=20, pady=5)
        setattr(self, f"{attr}_entry", entry)

    def create_opale_dropdown(self):
        ctk.CTkLabel(self, text="Opale :", anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        opale_titles = [title for _id, title in self.opale_list]
        self.opale_var = ctk.StringVar()
        current_id = str(self.task.opale or "")
        current_title = next((title for _id, title in self.opale_list if _id == current_id), current_id)
        self.opale_var.set(current_title)
        self.opale_menu = ctk.CTkOptionMenu(self, values=opale_titles, variable=self.opale_var)
        self.opale_menu.pack(fill="x", padx=20, pady=5)

    def save_task(self):
        updated_task = self.task.copy()
        updated_task["title"] = self.title_entry.get()
        updated_task["date"] = self.date_entry.get()
        updated_task["linkJira"] = self.linkJira_entry.get()
        updated_task["linkSpec"] = self.linkSpec_entry.get()
        updated_task["endDate"] = self.endDate_entry.get()

        selected_title = self.opale_var.get()
        selected_id = next((_id for _id, title in self.opale_list if title == selected_title), "0")
        try:
            updated_task["opale"] = int(selected_id)
        except ValueError:
            updated_task["opale"] = 0

        # Sauvegarde
        tasks = load_tasks()
        for t in tasks:
            if t["id"] == updated_task["id"]:
                t.update(updated_task)
                break
        save_tasks(tasks)

        self.refresh_callback()
        self.destroy()
