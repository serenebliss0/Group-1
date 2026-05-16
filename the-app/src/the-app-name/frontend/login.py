import tkinter as tk
from backend import login_handler, database

db_conn = database.Database()
handler = login_handler.LoginHandler(db_conn) # Instantiate the class and pass in the db_conn object

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0d0800")
        self.controller = controller

        tk.Label(self, text="THE RUIN AND THE GREEN", bg="#0d0800", fg="#C8541A",
                font=("Courier", 20, "bold")).pack(pady=(80, 5))

        tk.Label(self, text="sign in to continue", bg="#0d0800", fg="#b8a99a",
                font=("Courier", 10)).pack(pady=(0, 40))

        # Username
        tk.Label(self, text="USERNAME", bg="#0d0800", fg="#b8a99a",
                font=("Courier", 8)).pack()
        self.username_entry = tk.Entry(self, bg="#1a0a00", fg="#f5ead8",
            insertbackground="#f5ead8", font=("Courier", 11),
            relief="flat", width=30)
        self.username_entry.pack(pady=(4, 16), ipady=6)

        # Password
        tk.Label(self, text="PASSWORD", bg="#0d0800", fg="#b8a99a",
                font=("Courier", 8)).pack()
        self.password_entry = tk.Entry(self, bg="#1a0a00", fg="#f5ead8",
                                        insertbackground="#f5ead8", font=("Courier", 11),
                                        relief="flat", width=30, show="*")
        self.password_entry.pack(pady=(4, 24), ipady=6)

        # Feedback label
        self.feedback = tk.Label(self, text="", bg="#0d0800", fg="#C8541A",
                font=("Courier", 9))
        self.feedback.pack()

        # Buttons
        tk.Button(self, text="LOGIN", bg="#C8541A", fg="#f5ead8",
            font=("Courier", 10, "bold"), relief="flat", width=20,
            command=self.handle_login).pack(pady=(12, 6), ipady=6)

        tk.Button(self, text="CREATE ACCOUNT", bg="#1a0a00", fg="#b8a99a",
            font=("Courier", 9), relief="flat", width=20,
            command=lambda: controller.show_frame("SignupScreen")).pack(ipady=6)
        
        tk.Button(self, text="CREATE ACCOUNT", bg="#1a0a00", fg="#b8a99a",
                font=("Courier", 9), relief="flat", width=20,
                command=lambda: controller.show_frame("SignupScreen")).pack(ipady=6)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        stored_hash = handler.db.get_password_hash(username)

        if not username or not password:
            self.feedback.config(text="please fill in all fields.")
            return

            # Use the handler to get the hash
        stored_hash = handler.db.get_password_hash(username)

    # Call the method via the 'handler' instance
        if not stored_hash:
            self.feedback.config(text="user not found.")
            return

            # check password
        success = handler.check_password(password, stored_hash)

        if success:
            self.feedback.config(text="login successful.")
            self.controller.current_user = username
        # stop intro music later here if needed
        # self.controller.audio.stop()
            self.controller.show_frame("GameScreen")
        else:
            self.feedback.config(text="invalid username or password.")



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    root.configure(bg="#0d0800")
    app = LoginScreen(root, controller=None)
    app.pack(fill="both", expand=True)
    root.mainloop()