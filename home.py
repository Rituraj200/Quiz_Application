import tkinter as tk
from tkinter import ttk
from admin import AdminPanel  # Importing the AdminPanel class from admin.py
from user import QuizApp  # Importing the QuizApp class from 2.py (ensure the import path is correct)

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Home")
        self.root.geometry("800x600")
        # Maximizing the window and allowing resizing
        self.root.state('zoomed')  # This will maximize the window
        self.root.resizable(True, True)  # Allow resizing in both directions (horizontal and vertical)
        
        self.display_home_panel()

    def display_home_panel(self):
        """Display the Home Panel with buttons for Admin and User panels."""
        self.clear_screen()

        tk.Label(self.root, text="Home Panel", font=("Arial", 24, "bold")).pack(pady=30)

        # Buttons for navigation
        tk.Button(self.root, text="Go to Admin Panel", font=("Arial", 15), command=self.open_admin_panel).pack(pady=20)
        tk.Button(self.root, text="Go to User Panel", font=("Arial", 15), command=self.open_user_panel).pack(pady=20)

    def open_admin_panel(self):
        """Open the Admin Panel with an Exit button to return to Home."""
        self.clear_screen()
        admin_panel = AdminPanel(self.root)
        self.add_exit_button(self.display_home_panel)

    def open_user_panel(self):
        """Open the User Panel (QuizApp) with an Exit button to return to Home."""
        self.clear_screen()
        quiz_app = QuizApp(self.root)
        self.add_exit_button(self.display_home_panel)

    def add_exit_button(self, exit_command):
        """Add an Exit button to return to Home."""
        tk.Button(self.root, text="Back to Home", font=("Arial", 15), command=exit_command).pack(pady=20)

    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    home = Home(root)
    root.mainloop()
