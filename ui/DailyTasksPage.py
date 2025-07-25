import customtkinter as ctk
from datetime import datetime
from collections import defaultdict
import webbrowser

from managers.OpaleManager import load_opale_list
from model.Task import Task
from managers.TaskManager import load_tasks, save_tasks, finish_open_tasks
from ui.Autocomplete import SimpleAutocomplete
from utils.TimeUtils import compute_duration
from ui.TaskModal import TaskModal


class DailyTasksPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.display_tasks()

    def create_add_task_bar(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        self.task_entry = ctk.CTkEntry(form_frame, placeholder_text="Entrer une nouvelle tâche...")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        add_button = ctk.CTkButton(form_frame, text="Ajouter", command=self.add_task)
        add_button.pack(side="left", padx=5)

    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            return

        tasks = finish_open_tasks(load_tasks())
        new_task = Task(
            id=int(datetime.now().timestamp()),
            title=title,
            date=datetime.now().isoformat(timespec="seconds"),
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
        for task in tasks:
            if task.id == task_id and task.endDate is None:
                task.endDate = datetime.now()
        save_tasks(tasks)
        self.display_tasks()

    def update_opale(self, task, new_opale_title):
        opale_id = next((int(_id) for _id, title in load_opale_list() if title == new_opale_title), 0)
        task.opale = opale_id
        tasks = load_tasks()
        for t in tasks:
            if t.id == task.id:
                t.opale = opale_id
        save_tasks(tasks)

    def display_tasks(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_add_task_bar()
        tasks_by_date = defaultdict(list)
        for task in load_tasks():
            date_str = task.date.strftime("%Y-%m-%d") if task.date else "?"
            tasks_by_date[date_str].append(task)

        for date_str in sorted(tasks_by_date.keys(), reverse=True):
            date_label = ctk.CTkLabel(self, text=date_str, font=("Arial", 16, "bold"))
            date_label.pack(anchor="w", padx=10, pady=5)

            for task in tasks_by_date[date_str]:
                self.create_task_row(task)

    def create_task_row(self, task):
        row_frame = ctk.CTkFrame(self)
        row_frame.pack(fill="x", padx=10, pady=2)

        if task.endDate:
            duration = compute_duration(task.date, task.endDate)
            ctk.CTkLabel(row_frame, text=duration, width=80).pack(side="left", padx=5)
        else:
            ctk.CTkButton(row_frame, text="Finir", width=60,
                          command=lambda tid=task.id: self.finish_task(tid))\
                .pack(side="left", padx=5)

        title_label = ctk.CTkLabel(row_frame, text=task.title, cursor="hand2")
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", lambda e, t=task: self.open_modal(t))
        title_label.bind("<Enter>", lambda e, lbl=title_label: lbl.configure(font=("Arial", 12, "underline")))
        title_label.bind("<Leave>", lambda e, lbl=title_label: lbl.configure(font=("Arial", 12, "normal")))

        opale_titles = [title for _id, title in load_opale_list()]
        current_title = next((title for _id, title in load_opale_list() if int(_id) == task.opale), "")
        autocomplete = SimpleAutocomplete(row_frame, opale_titles)
        autocomplete.pack(side="left", padx=5)
        if current_title:
            autocomplete.entry.insert(0, current_title)
        autocomplete.entry.bind("<FocusOut>", lambda e, t=task, a=autocomplete: self.update_opale(t, a.get()))

        if task.linkJira:
            ctk.CTkButton(row_frame, text="JIRA", width=60,
                          command=lambda url=task.linkJira: self.open_link(url)).pack(side="left", padx=5)
        if task.linkSpec:
            ctk.CTkButton(row_frame, text="Spec", width=60,
                          command=lambda url=task.linkSpec: self.open_link(url)).pack(side="left", padx=5)

    def open_modal(self, task):
        TaskModal(self, task, refresh_callback=self.display_tasks)

    def open_link(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Erreur ouverture lien: {e}")
