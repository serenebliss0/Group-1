import tkinter as tk
from tkinter import font
from backend import login_handler, database, session, logic

db_conn = database.Database()
handler = login_handler.LoginHandler(db_conn)


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0d0800")
        self.controller = controller

        # =========================
        # ROOT GRID (TRUE CENTERING)
        # =========================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # =========================
        # LEFT SIDE (CENTERED)
        # =========================
        left = tk.Frame(self, bg="#0d0800")
        left.grid(row=0, column=0, sticky="nsew")

        left_center = tk.Frame(left, bg="#0d0800")
        left_center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            left_center,
            text="What\nRemains?",
            bg="#0d0800",
            fg="#C8541A",
            font=("Playfair Display", 60, "bold"),  # ✅ ORIGINAL SIZE RESTORED
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            left_center,
            text="A narrative game",
            bg="#0d0800",
            fg="#b8a99a",
            font=("Courier", 10)
        ).pack(anchor="w", pady=(6, 10))

        tk.Label(
            left_center,
            text="You are a citizen of a dying city making\nimpossible decisions.\n\nUntil you realise you are not a citizen at all.",
            bg="#0d0800",
            fg="#b8a99a",
            font=("Courier", 9),
            justify="left"
        ).pack(anchor="w")

        # =========================
        # RIGHT SIDE (CENTERED LOGIN CARD)
        # =========================
        right = tk.Frame(self, bg="#0d0800")
        right.grid(row=0, column=1, sticky="nsew")

        right_center = tk.Frame(right, bg="#0d0800")
        right_center.place(relx=0.5, rely=0.5, anchor="center")

        # LOGIN CARD (WIDER LIKE YOUR IMAGE)
        card = tk.Frame(
            right_center,
            bg="#120a05",
            highlightbackground="#3a2a20",
            highlightthickness=1
        )
        card.pack()

        # FIXED SIZE (THIS WAS TOO THIN BEFORE)
        card.config(width=420, height=380)
        card.pack_propagate(False)

        tk.Label(
            card,
            text="LOGIN",
            bg="#120a05",
            fg="#b8a99a",
            font=("Courier", 12, "bold")
        ).pack(pady=(30, 12))

        # Username
        tk.Label(card, text="USERNAME", bg="#120a05", fg="#b8a99a",
                 font=("Courier", 8)).pack()

        self.username_entry = tk.Entry(
            card,
            bg="#c1c1c1",
            fg="#000000",
            insertbackground="#000000",
            font=("Courier", 11),
            relief="flat",
            width=30
        )
        self.username_entry.pack(pady=(6, 14), ipady=6)

        # Password
        tk.Label(card, text="PASSWORD", bg="#120a05", fg="#b8a99a",
                 font=("Courier", 8)).pack()

        self.password_entry = tk.Entry(
            card,
            bg="#c1c1c1",
            fg="#000000",
            insertbackground="#000000",
            font=("Courier", 11),
            relief="flat",
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=(6, 16), ipady=6)

        # Feedback
        self.feedback = tk.Label(
            card,
            text="",
            bg="#120a05",
            fg="#C8541A",
            font=("Courier", 9)
        )
        self.feedback.pack()

        # Buttons
        tk.Button(
            card,
            text="LOGIN",
            bg="#C8541A",
            fg="#f5ead8",
            font=("Courier", 10, "bold"),
            relief="flat",
            width=22,
            command=self.handle_login
        ).pack(pady=(14, 6), ipady=6)

        tk.Button(
            card,
            text="CREATE AN ACCOUNT",
            bg="#1a0a00",
            fg="#b8a99a",
            font=("Courier", 9),
            relief="flat",
            width=22,
            command=lambda: controller.show_frame("SignupScreen")
        ).pack(ipady=6)

        tk.Button(
            card,
            text="I forgot my name",
            bg="#1a0a00",
            fg="#b8a99a",
            font=("Courier", 8),
            relief="flat",
            width=22,
            command=lambda: self.on_click_forgot_name()
        ).pack(pady=(8, 12), ipady=4)

    # =========================
    # LOGIC (UNCHANGED)
    # =========================
    def on_click_forgot_name(self):
        self.controller.show_frame("SignupScreen")
        logic.wtf_value += 10

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.feedback.config(text="please fill in all fields.")
            return

        stored_hash = handler.db.get_password_hash(username)

        if not stored_hash:
            self.feedback.config(text="user not found.")
            return

        success = handler.check_password(password, stored_hash)

        if success:
            self.feedback.config(text="login successful.")
            self.controller.current_user = username
            session.save_session(username)
            self.controller.show_frame("MainMenu")
        else:
            self.feedback.config(text="invalid username or password.")