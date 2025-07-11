import customtkinter as ctk
from collections import defaultdict
from datetime import datetime

from managers.TaskManager import load_tasks
from managers.OpaleManager import load_opale_titles
from utils.TimeUtils import compute_duration_minutes, format_duration

class MonthlySummaryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.opale_titles = load_opale_titles()

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_summary()

    def display_summary(self):
        # Clear old content
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = load_tasks()
        summary = defaultdict(lambda: defaultdict(int))  # { date: { opale: total_minutes } }

        for task in tasks:
            start = task.date.isoformat() if task.date else None
            end = task.endDate.isoformat() if task.endDate else None
            opale = str(task.opale or "0")

            if start and end:
                try:
                    day = task.date.strftime("%Y-%m-%d")
                    duration = compute_duration_minutes(start, end)
                    summary[day][opale] += duration
                except:
                    continue

        # Display
        row = 0
        for day in sorted(summary.keys(), reverse=True):
            day_label = ctk.CTkLabel(self.scroll_frame, text=f"{day}", font=("Arial", 16, "bold"))
            day_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
            row += 1

            for opale, total_minutes in summary[day].items():
                duration_text = format_duration(total_minutes)
                opale_title = self.opale_titles.get(opale, f"Opale: {opale}")

                duration_label = ctk.CTkLabel(self.scroll_frame, text=duration_text)
                duration_label.grid(row=row, column=0, padx=20, pady=2, sticky="w")

                opale_label = ctk.CTkLabel(self.scroll_frame, text=opale_title)
                opale_label.grid(row=row, column=1, padx=20, pady=2, sticky="w")

                row += 1
