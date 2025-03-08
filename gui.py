import os
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk
import ttkbootstrap as ttk


class App:
    def __init__(self, app_controller):
        """Initialize the GUI and receive an app instance for handling logic."""
        self.app_controller = app_controller
        self.screenshot_folder = self.app_controller.get_screenshot_folder()

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.screenshot_folder = folder_selected
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, self.screenshot_folder)
            self.app_controller.set_screenshot_folder(self.screenshot_folder)

    def show_version_info(self):
        messagebox.showinfo("Version Info", "HLL Map Screenshot v0.02\nCreated by Dominik Majchrzak\nMIT License")

    def create_gui(self):
        root = ThemedTk()
        root.title("HLL Map Screenshot")
        root.geometry("500x200")
        root.iconbitmap(os.path.join("Icon", "sso.ico"))
        root.configure(bg="#2E2E2E")

        style = ttk.Style()
        style.theme_use("darkly")
        style.configure("TButton", font=("Arial", 14))
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="white")
        style.configure("TEntry", fieldbackground="#2E2E2E", foreground="white", insertbackground="white")

        main_frame = ttk.Frame(root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Start button for HLL detection
        self.start_button = ttk.Button(main_frame, text="Start", bootstyle="danger",
                                       command=lambda: self.app_controller.toggle_hll_detection(self.start_button))
        self.start_button.pack(pady=10, ipadx=10, ipady=5)

        # Folder selection controls
        folder_label = ttk.Label(main_frame, text="Screenshot save folder:", style="TLabel")
        folder_label.pack()

        folder_frame = ttk.Frame(main_frame, style="TFrame")
        folder_frame.pack(fill=tk.X, pady=5)

        folder_border_frame = tk.Frame(folder_frame, background="white",
                                       highlightbackground="white", highlightthickness=2)
        folder_border_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        self.folder_entry = ttk.Entry(folder_border_frame, width=50, bootstyle="dark")
        self.folder_entry.insert(0, self.screenshot_folder)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_button = ttk.Button(folder_frame, text="Browse", command=self.select_folder)
        browse_button.pack(side=tk.RIGHT, padx=5)

        info_button = ttk.Button(root, text="ℹ️", command=self.show_version_info,
                                 bootstyle="secondary", width=1, padding=(8, 4))
        info_button.place(relx=0.98, rely=0.95, anchor="se")

        root.mainloop()
