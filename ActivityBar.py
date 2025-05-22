import tkinter as tk

class ActivityBar:
    def __init__(self, parent):
        self.parent = parent
        self.project_manager_visible = False

        # Activity bar on the far left
        self.activity_bar = tk.Frame(self.parent.window, width=80, bg="black")
        self.activity_bar.pack(side="left", fill="y")

        # Sidebar Frame (initially hidden but packed before notebook)
        self.project_frame = tk.Frame(self.parent.window, width=200, bg="white")
        self.project_frame.pack(side="left", fill="y")
        self.project_frame.pack_forget()  # Hide it initially

        # Button to toggle sidebar
        self.files_btn = tk.Button(
            self.activity_bar,
            text="Project Manager",
            command=self.toggle_project_manager
        )
        self.files_btn.pack(pady=10, padx=10)

    def toggle_project_manager(self):
        if self.project_manager_visible:
            self.project_frame.pack_forget()
            self.project_manager_visible = False
            self.files_btn.config(relief="raised")
        else:
            self.project_frame.pack(side="left", fill="y")
            self.project_manager_visible = True
            self.files_btn.config(relief="sunken")
