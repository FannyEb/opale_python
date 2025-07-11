import customtkinter as ctk
from datetime import datetime
from collections import defaultdict
import webbrowser

from model.Task import Task
from managers.TaskManager import load_tasks, save_tasks, finish_open_tasks
from utils.TimeUtils import compute_duration
from ui.TaskModal import TaskModal

class DailyTasksPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

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

    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            return

        tasks = load_tasks()
        tasks = finish_open_tasks(tasks)

        new_task = Task(
            id=int(datetime.now().timestamp()),
            title=title,
            date=datetime.now().isoformat(timespec='minutes'),
            linkJira=None,
            linkSpec=None,
            opale=0,
            endDate=None
        )

        tasks.append(new_task)
        save_tasks(tasks)

        self.task_entry.delete(0, ctk.END)
        self.display_tasks()

    def finish_task(self, task_id):
        tasks = load_tasks()
        now = datetime.now()

        for task in tasks:
            if task.id == task_id and task.endDate is None:
                task.endDate = now

        save_tasks(tasks)
        self.display_tasks()

    def display_tasks(self):
        # Nettoyer le scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = load_tasks()
        tasks_by_date = defaultdict(list)

        for task in tasks:
            date_str = task.date.strftime("%Y-%m-%d") if task.date else "?"
            tasks_by_date[date_str].append(task)

        row = 0
        for date_str in sorted(tasks_by_date.keys(), reverse=True):
            day_label = ctk.CTkLabel(self.scroll_frame, text=f"{date_str}", font=("Arial", 16, "bold"))
            day_label.grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=5)
            row += 1

            for task in tasks_by_date[date_str]:
                # Durée ou bouton finir
                if task.endDate:
                    duration_text = compute_duration(task.date, task.endDate)
                    duration_label = ctk.CTkLabel(self.scroll_frame, text=duration_text)
                    duration_label.grid(row=row, column=0, padx=10, sticky="w")
                else:
                    finish_btn = ctk.CTkButton(self.scroll_frame, text="Finir", width=60,
                                               command=lambda tid=task.id: self.finish_task(tid))
                    finish_btn.grid(row=row, column=0, padx=10, pady=2, sticky="w")

                # Titre cliquable
                title_label = ctk.CTkLabel(self.scroll_frame, text=task.title, text_color="#2e6de3", cursor="hand2")
                title_label.grid(row=row, column=1, padx=20, pady=2, sticky="w")
                title_label.bind("<Button-1>", lambda e, t=task: self.open_modal(t))
                # Hover
                def on_enter(e, lbl=title_label):
                    lbl.configure(font=("Arial", 12, "underline"))
                def on_leave(e, lbl=title_label):
                    lbl.configure(font=("Arial", 12, "normal"))
                title_label.bind("<Enter>", on_enter)
                title_label.bind("<Leave>", on_leave)

                # Boutons JIRA & Spec
                col = 2
                if task.linkJira:
                    jira_btn = ctk.CTkButton(self.scroll_frame, text="JIRA", width=60,
                                             command=lambda url=task.linkJira: self.open_link(url))
                    jira_btn.grid(row=row, column=col, padx=5, pady=2)
                    col += 1
                if task.linkSpec:
                    spec_btn = ctk.CTkButton(self.scroll_frame, text="Spec", width=60,
                                             command=lambda url=task.linkSpec: self.open_link(url))
                    spec_btn.grid(row=row, column=col, padx=5, pady=2)

                row += 1

    def open_modal(self, task):
        TaskModal(self, task, refresh_callback=self.display_tasks)


    def open_link(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Erreur ouverture lien: {e}")
