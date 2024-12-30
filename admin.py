import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.users_scores = self.load_scores()
        self.admin_login_screen()

    def load_scores(self):
        """Load user scores from a file"""
        if os.path.exists("user_scores.json"):
            with open("user_scores.json", "r") as file:
                return json.load(file)
        return {}

    def save_scores(self):
        """Save user scores to a file"""
        with open("user_scores.json", "w") as file:
            json.dump(self.users_scores, file, indent=4)

    def admin_login_screen(self):
        """Admin login screen"""
        self.clear_screen()

        tk.Label(self.root, text="Admin Login", font=("Arial", 30, "bold")).pack(pady=20)

        # Create a frame for the login fields and center it
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=30)

        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=3)

        # Add username field and label
        tk.Label(login_frame, text="Username:", font=("Arial", 15)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.admin_username_entry = tk.Entry(login_frame, font=("Arial", 15))
        self.admin_username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Add password field and label
        tk.Label(login_frame, text="Password:", font=("Arial", 15)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.admin_password_entry = tk.Entry(login_frame, font=("Arial", 15), show="*")
        self.admin_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Add login button
        login_button = tk.Button(login_frame, text="Login", font=("Arial", 15), command=self.admin_login)
        login_button.grid(row=2, columnspan=2, pady=20)

    def admin_login(self):
        """Authenticate admin login"""
        admin_username = self.admin_username_entry.get()
        admin_password = self.admin_password_entry.get()

        if admin_username == "admin" and admin_password == "admin123":
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials!")

    def admin_panel(self):
        """Admin control panel to manage users"""
        self.clear_screen()

        tk.Label(self.root, text="Admin Panel", font=("Arial", 30, "bold")).pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20, fill="x")

        tk.Button(button_frame, text="View All Users", font=("Arial", 15), command=self.view_users).pack(fill="x", pady=10)
        tk.Button(button_frame, text="Create User", font=("Arial", 15), command=self.create_user).pack(fill="x", pady=10)
        tk.Button(button_frame, text="Delete User", font=("Arial", 15), command=self.delete_user).pack(fill="x", pady=10)
        tk.Button(button_frame, text="Delete All Users", font=("Arial", 15), command=self.delete_all_users).pack(fill="x", pady=10)
        tk.Button(button_frame, text="Exit", font=("Arial", 15), command=self.exit_admin).pack(fill="x", pady=10)

    def delete_all_users(self):
        """Delete all users and their quiz history"""
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all users and their quiz history?")
        if confirm:
            self.users_scores.clear()
            self.save_scores()
            messagebox.showinfo("Success", "All users and quiz history have been deleted successfully!")
            self.admin_panel()

    def view_users(self):
        """Display all users with numbering and scrollbar"""
        self.clear_screen()

        tk.Label(self.root, text="All Users", font=("Arial", 30, "bold")).pack(pady=20)

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for idx, user in enumerate(self.users_scores.keys(), 1):
            tk.Label(scrollable_frame, text=f"{idx}. {user}", font=("Arial", 15)).pack(pady=5, anchor="w")

        tk.Button(self.root, text="Back", font=("Arial", 15), command=self.admin_panel).place(relx=1.0, rely=0.05, anchor="ne")

    def create_user(self):
        """Create a new user with a username and password"""
        self.clear_screen()

        tk.Label(self.root, text="Create User", font=("Arial", 30, "bold")).pack(pady=20)

        # Create a frame for the form
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)

        # Username field
        tk.Label(form_frame, text="Username:", font=("Arial", 15)).grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(form_frame, font=("Arial", 15))
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password field
        tk.Label(form_frame, text="Password:", font=("Arial", 15)).grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(form_frame, font=("Arial", 15), show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        def save_user():
            """Save the new user with the provided username and password"""
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showerror("Error", "Username and Password cannot be empty!")
                return

            if username in self.users_scores:
                messagebox.showerror("Error", "User already exists!")
            else:
                # Add the new user with the provided username and password
                self.users_scores[username] = {"password": password, "Python": 0, "DSA": 0, "DBMS": 0}
                self.save_scores()
                messagebox.showinfo("Success", "User created successfully!")
                self.admin_panel()  # Return to the admin panel

        # Save button to create the user
        tk.Button(form_frame, text="Save", font=("Arial", 15), command=save_user).grid(row=2, columnspan=2, pady=20)

        # Back button to return to the admin panel
        tk.Button(self.root, text="Back", font=("Arial", 15), command=self.admin_panel).place(relx=1.0, rely=0.05, anchor="ne")

    def delete_user(self):
        """Delete an existing user"""
        self.clear_screen()

        tk.Label(self.root, text="Delete User", font=("Arial", 30, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username:", font=("Arial", 15)).grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(form_frame, font=("Arial", 15))
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        def remove_user():
            username = username_entry.get()
            if username not in self.users_scores:
                messagebox.showerror("Error", "User does not exist!")
            else:
                del self.users_scores[username]
                self.save_scores()
                messagebox.showinfo("Success", "User deleted successfully!")
                self.admin_panel()

        tk.Button(form_frame, text="Delete", font=("Arial", 15), command=remove_user).grid(row=1, columnspan=2, pady=20)

        tk.Button(self.root, text="Back", font=("Arial", 15), command=self.admin_panel).place(relx=1.0, rely=0.05, anchor="ne")

    def exit_admin(self):
        """Exit the admin panel"""
        self.root.quit()

    def clear_screen(self):
        """Clear the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    admin_panel = AdminPanel(root)
    root.mainloop()
