import tkinter as tk

BG = "#1a0a00"
EMBER = "#C8541A"
CREAM = "#f5ead8"
DIM = "#4a3728"


class DialogueOverlay(tk.Toplevel):

    def __init__(self, parent, data):

        super().__init__(parent)

        self.parent = parent
        self.data = data

        self.configure(bg=BG)

        self.geometry("700x350")

        self.overrideredirect(True)

        self.transient(parent)

        self.grab_set()

        self._center()

        self._build_ui()

    def _center(self):

        self.update_idletasks()

        w = 700
        h = 350

        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):

        frame = tk.Frame(
            self,
            bg=BG,
            highlightbackground=EMBER,
            highlightthickness=3
        )

        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = tk.Label(
            frame,
            text=self.data["name"],
            bg=BG,
            fg=CREAM,
            font=("Courier", 20, "bold")
        )

        title.pack(pady=(20, 10))

        body = tk.Label(
            frame,
            text=self.data["text"],
            bg=BG,
            fg=CREAM,
            wraplength=550,
            justify="left",
            font=("Courier", 12)
        )

        body.pack(pady=10)

        button_frame = tk.Frame(frame, bg=BG)

        button_frame.pack(side="bottom", pady=20)

        choice_a = tk.Button(
            button_frame,
            text=self.data["choice_a"],
            command=self._fix_problem,
            bg=EMBER,
            fg=CREAM,
            relief="flat",
            font=("Courier", 11, "bold"),
            padx=12,
            pady=8
        )

        choice_a.grid(row=0, column=0, padx=10)

        choice_b = tk.Button(
            button_frame,
            text=self.data["choice_b"],
            command=self.destroy,
            bg=DIM,
            fg=CREAM,
            relief="flat",
            font=("Courier", 11),
            padx=12,
            pady=8
        )

        choice_b.grid(row=0, column=1, padx=10)

        choice_c = tk.Button(
            button_frame,
            text=self.data["choice_c"],
            command=self.destroy,
            bg="#000000",
            fg=CREAM,
            relief="flat",
            font=("Courier", 11),
            padx=12,
            pady=8
        )

        choice_c.grid(row=0, column=2, padx=10)

    def _fix_problem(self):

        scenario_id = self.data["id"]

        for node in self.parent.interactive_nodes:

            if node["id"] == scenario_id:

                if node["fixed"]:
                    return

                node["fixed"] = True

                self.parent.canvas.create_text(
                    node["x"],
                    node["y"] - 80,
                    text="✔",
                    fill="lime",
                    font=("Arial", 34, "bold")
                )

        self.destroy()