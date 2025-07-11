import customtkinter as ctk
from tkinter import messagebox

from managers.OpaleManager import load_opale_list
from managers.TaskManager import load_tasks, save_tasks
from ui.Autocomplete import SimpleAutocomplete

class TaskModal(ctk.CTkToplevel):
    def __init__(self, master, task, refresh_callback):
        super().__init__(master)

        self.transient(master)
        self.grab_set()
        self.focus()
        self.focus_force()

        self.title("Détails de la tâche")
        self.geometry("450x600")

        self.task = task
        self.refresh_callback = refresh_callback

        # Charger la liste Opale
        self.opale_list = load_opale_list()

        # SCROLLABLE FRAME
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=420, height=580)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_ui()

    def build_ui(self):
        self.create_labeled_entry("Titre :", "title", self.task.title)
        self.create_labeled_entry("Date de début (ISO) :", "date", self.task.date)
        self.create_labeled_entry("Lien JIRA :", "linkJira", self.task.linkJira or "")
        self.create_labeled_entry("Lien SPEC :", "linkSpec", self.task.linkSpec or "")

        # AUTOCOMPLETE OPALE
        ctk.CTkLabel(self.scroll_frame, text="Opale :", anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        opale_titles = [title for _id, title in self.opale_list]
        self.opale_autocomplete = SimpleAutocomplete(self.scroll_frame, opale_titles)
        self.opale_autocomplete.pack(fill="x", padx=20, pady=5)

        # Pré-sélection si possible
        current_id = str(self.task.opale or "")
        current_title = next((title for _id, title in self.opale_list if _id == current_id), "")
        self.opale_autocomplete.entry.insert(0, current_title)

        self.create_labeled_entry("Date de fin (ISO) :", "endDate", self.task.endDate or "")

        save_btn = ctk.CTkButton(self.scroll_frame, text="Sauvegarder", command=self.save_task)
        save_btn.pack(pady=20)

    def create_labeled_entry(self, label_text, attr_name, initial_value):
        ctk.CTkLabel(self.scroll_frame, text=label_text, anchor="w").pack(fill="x", padx=20, pady=(15, 0))
        entry = ctk.CTkEntry(self.scroll_frame)
        entry.insert(0, initial_value)
        entry.pack(fill="x", padx=20, pady=5)
        setattr(self, f"{attr_name}_entry", entry)

    def save_task(self):
        tasks = load_tasks()
        for t in tasks:
            if t.id == self.task.id:
                t.title = self.title_entry.get()
                t.date = self.date_entry.get()
                t.linkJira = self.linkJira_entry.get()
                t.linkSpec = self.linkSpec_entry.get()

                selected_title = self.opale_autocomplete.get()
                selected_id = next((_id for _id, title in self.opale_list if title == selected_title), "0")
                t.opale = int(selected_id)

                t.endDate = self.endDate_entry.get()
                break

        save_tasks(tasks)
        self.refresh_callback()
        self.destroy()