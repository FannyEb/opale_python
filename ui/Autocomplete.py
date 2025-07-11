import customtkinter as ctk

class SimpleAutocomplete(ctk.CTkFrame):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.values = values
        self.selected_value = None

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(fill="x")
        self.entry.bind("<KeyRelease>", self.update_suggestions)

        self.suggestions_frame = None  # ne pas créer tout de suite

    def update_suggestions(self, event):
        # Détruire l'ancien frame s'il existe
        if self.suggestions_frame:
            self.suggestions_frame.destroy()
            self.suggestions_frame = None

        typed = self.entry.get().lower()
        if not typed:
            return

        filtered = [v for v in self.values if typed in v.lower()]
        if not filtered:
            return

        # Créer suggestions_frame seulement si nécessaire
        self.suggestions_frame = ctk.CTkFrame(self)
        self.suggestions_frame.pack(fill="x")

        for suggestion in filtered[:5]:
            btn = ctk.CTkButton(self.suggestions_frame, text=suggestion, width=200,
                                command=lambda s=suggestion: self.select_value(s))
            btn.pack(pady=2)

    def select_value(self, value):
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, value)
        self.selected_value = value

        if self.suggestions_frame:
            self.suggestions_frame.destroy()
            self.suggestions_frame = None

        self.master.focus_set()


    def get(self):
        return self.entry.get().strip()
