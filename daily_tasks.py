import customtkinter as ctk
import json
import os
from datetime import datetime
from collections import defaultdict
from fileHelper import get_data_folder
from task_modal import TaskModal

class DailyTasksPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.json_path = os.path.join(get_data_folder(), "tasks.json")

        # Entrée pour ajouter une tâche
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        self.task_entry = ctk.CTkEntry(form_frame, placeholder_text="Entrer une nouvelle tâche...")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5)

        add_button = ctk.CTkButton(form_frame, text="Ajouter", command=self.add_task)
        add_button.pack(side="left", padx=5)

        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Scroll pour les tâches
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=350)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_tasks()

    def compute_duration(self, start_str, end_str):
        try:
            start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
            delta = end_dt - start_dt
            total_minutes = int(delta.total_seconds() // 60)
            hours, minutes = divmod(total_minutes, 60)
            return f"{hours:02d}:{minutes:02d}"
        except:
            return "--:--"

    def add_task(self):
        self.json_path = os.path.join(get_data_folder(), "tasks.json")

        title = self.task_entry.get().strip()
        if title == "":
            return

        # Terminer toutes les tâches ouvertes avant d'en ajouter une nouvelle
        self.finish_open_tasks()

        now_iso = datetime.now().isoformat(timespec='minutes')
        new_task = {
            "id": int(datetime.now().timestamp()),
            "title": title,
            "date": now_iso,
            "linkJira": None,
            "linkSpec": None,
            "opale": 0,
            "endDate": None
        }

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []

        tasks.append(new_task)
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

        self.task_entry.delete(0, ctk.END)
        self.display_tasks()

    def finish_open_tasks(self):
        now_iso = datetime.now().isoformat(timespec='minutes')
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []

        updated = False
        for task in tasks:
            if task.get("endDate") in [None, ""]:
                task["endDate"] = now_iso
                updated = True

        if updated:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)

    def finish_task(self, task_id):
        now_iso = datetime.now().isoformat(timespec='minutes')
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []

        for task in tasks:
            if task["id"] == task_id and task.get("endDate") in [None, ""]:
                task["endDate"] = now_iso

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

        self.display_tasks()

    def display_tasks(self):
        self.json_path = os.path.join(get_data_folder(), "tasks.json")

        # Nettoyer
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []

        tasks_by_date = defaultdict(list)
        for task in tasks:
            try:
                parsed_date = datetime.fromisoformat(task.get("date", "").replace("Z", "+00:00"))
                date_str = parsed_date.strftime("%Y-%m-%d")
            except:
                date_str = task.get("date", "")
            tasks_by_date[date_str].append(task)

        row = 0
        for date_str in sorted(tasks_by_date.keys(), reverse=True):
            day_label = ctk.CTkLabel(self.scroll_frame, text=f"{date_str}", font=("Arial", 16, "bold"))
            day_label.grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=5)
            row += 1

            for task in tasks_by_date[date_str]:
                # Durée ou bouton "Finir"
                if task.get("endDate"):
                    duration_text = self.compute_duration(task.get("date"), task.get("endDate"))
                    duration_label = ctk.CTkLabel(self.scroll_frame, text=duration_text)
                    duration_label.grid(row=row, column=0, padx=10, sticky="w")
                else:
                    finish_btn = ctk.CTkButton(self.scroll_frame, text="Finir", width=60,
                                               command=lambda tid=task["id"]: self.finish_task(tid))
                    finish_btn.grid(row=row, column=0, padx=10, pady=2, sticky="w")

                # Titre cliquable
                title_label = ctk.CTkLabel(self.scroll_frame, text=task.get("title", ""))
                title_label.grid(row=row, column=1, padx=20, pady=2, sticky="w")
                title_label.bind("<Button-1>", lambda e, t=task: self.open_modal(t))

                row += 1

    def open_modal(self, task):
        TaskModal(self, task, self.json_path, self.display_tasks)
