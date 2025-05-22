import tkinter as tk

class MenuBar:

    def __init__(self, parent):
        self.parent = parent
        self.menu = tk.Menu(self.parent.window)
        self.parent.window.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Text File", command=self.parent.new_text_file)
        self.file_menu.add_command(label="New File", command=self.parent.new_text_file)
        self.file_menu.add_command(label="New Window", command=self.parent.open_new_window)
        self.file_menu.add_separator()

        self.file_menu.add_command(label="Open File", command=self.parent.open_file)
        self.file_menu.add_command(label="Open Folder", command=self.parent.open_file)
        self.file_menu.add_command(label="Open Workspace from File", command=self.parent.open_file)
        self.file_menu.add_command(label="Open recent", command=self.parent.open_file)
        self.file_menu.add_separator()

        self.file_menu.add_command(label="Save ", command=self.parent.save_as_file)
        self.file_menu.add_command(label="Save As", command=self.parent.save_as_file)
        self.file_menu.add_command(label="New Window", command=self.parent.open_new_window)
        self.file_menu.add_separator()

        self.file_menu.add_command(label="Revert File", command=self.parent.open_new_window)
        self.file_menu.add_command(label="Close Editor", command=self.parent.open_new_window)
        self.file_menu.add_command(label="Close Folder", command=self.parent.open_new_window)
        self.file_menu.add_command(label="Close Window", command=self.parent.open_new_window)
        self.file_menu.add_separator()

        self.file_menu.add_command(label="Exit", command=self.parent.window.quit)


        self.menu.add_cascade(label="Edit", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="Selection", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="View", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="Go", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="Run", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="Terminal", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="Help", menu=tk.Menu(self.menu, tearoff=0))