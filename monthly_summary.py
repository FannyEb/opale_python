import customtkinter as ctk
import json
import os
from datetime import datetime
from collections import defaultdict

from fileHelper import get_data_folder

class MonthlySummaryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.json_path = os.path.join(get_data_folder(), "tasks.json")
        self.opale_titles = self.load_opale_titles()

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_summary()

    def load_opale_titles(self):
        opale_path = os.path.join(get_data_folder(), "opale.json")
        try:
            with open(opale_path, "r", encoding="utf-8") as f:
                opale_list = json.load(f)
            return { str(item["id"]): item.get("title", f"Opale {item['id']}") for item in opale_list }
        except FileNotFoundError:
            return {}

    def compute_duration_minutes(self, start_str, end_str):
        try:
            start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
            delta = end_dt - start_dt
            return int(delta.total_seconds() // 60)
        except:
            return 0

    def format_duration(self, total_minutes):
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours:02d}:{minutes:02d}"

    def display_summary(self):
        # Clear old content
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            tasks = []

        summary = defaultdict(lambda: defaultdict(int))  # { date: { opale: total_minutes } }

        for task in tasks:
            start = task.get("date")
            end = task.get("endDate")
            opale = str(task.get("opale") or "0")

            if start and end:
                try:
                    day = datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%Y-%m-%d")
                    duration = self.compute_duration_minutes(start, end)
                    summary[day][opale] += duration
                except:
                    continue

        # Afficher
        row = 0
        for day in sorted(summary.keys(), reverse=True):
            day_label = ctk.CTkLabel(self.scroll_frame, text=f"{day}", font=("Arial", 16, "bold"))
            day_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)
            row += 1

            for opale, total_minutes in summary[day].items():
                duration_text = self.format_duration(total_minutes)
                opale_title = self.opale_titles.get(opale, f"Opale: {opale}")

                duration_label = ctk.CTkLabel(self.scroll_frame, text=duration_text)
                duration_label.grid(row=row, column=0, padx=20, pady=2, sticky="w")

                opale_label = ctk.CTkLabel(self.scroll_frame, text=opale_title)
                opale_label.grid(row=row, column=1, padx=20, pady=2, sticky="w")

                row += 1
