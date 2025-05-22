import tkinter as tk
from tkinter import ttk
import os

class ActivityBar:
    def __init__(self, parent):
        self.parent = parent

        # Main activity bar on left
        self.activity_bar = tk.Frame(self.parent.window, width=80, bg="black")
        self.activity_bar.pack(side="left", fill="y")

        # White separator line between activity bar and side panels
        self.separator = tk.Frame(self.parent.window, width=2, bg="white")
        self.separator.pack(side="left", fill="y")

        # Dictionary to hold button frames
        self.frames = {}

        # Dictionary to hold buttons and their state
        self.buttons = {}

        # Example buttons and their frames
        self.create_button_with_frame("Project Manager", self.create_project_manager_frame)
        self.create_button_with_frame("Search", self.create_search_frame)
        self.create_button_with_frame("Settings", self.create_settings_frame)

    def create_button_with_frame(self, name, frame_creator):
        # Button in activity bar
        btn = tk.Button(self.activity_bar, text=name, wraplength=70, command=lambda n=name: self.toggle_frame(n))
        btn.pack(pady=10, padx=10)
        self.buttons[name] = btn

        # Create the frame (but do not pack)
        frame = frame_creator()
        frame.pack_forget()
        self.frames[name] = frame

    def toggle_frame(self, name):
        for fname, frame in self.frames.items():
            if fname == name:
                if frame.winfo_ismapped():
                    frame.pack_forget()
                    self.buttons[name].config(relief="raised")
                else:
                    # Pack sidebar frame after separator with some left padding
                    frame.pack(side="left", fill="y")
                    self.buttons[name].config(relief="sunken")
            else:
                frame.pack_forget()
                self.buttons[fname].config(relief="raised")

    # Create the project manager frame with a treeview
    def create_project_manager_frame(self):
        frame = tk.Frame(self.parent.window, width=200, bg="black")

        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background="black",
                        foreground="white",
                        fieldbackground="black",
                        bordercolor="black",
                        borderwidth=0)
        style.map("Custom.Treeview",
                  background=[('selected', '#3465A4')],
                  foreground=[('selected', 'white')])

        tree = ttk.Treeview(frame, style="Custom.Treeview")
        tree["show"] = "tree"
        tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vsb.set)

        root_node = tree.insert('', 'end', text=os.getcwd(), open=True)
        self._populate_tree(tree, root_node, os.getcwd())

        tree.bind('<<TreeviewOpen>>', lambda e: self.on_open_node(tree, e))

        return frame

    def _populate_tree(self, tree, parent, path):
        try:
            for p in os.listdir(path):
                abspath = os.path.join(path, p)
                isdir = os.path.isdir(abspath)
                node = tree.insert(parent, 'end', text=p, open=False)
                if isdir:
                    tree.insert(node, 'end', text="Loading...")
        except PermissionError:
            pass

    def on_open_node(self, tree, event):
        node = tree.focus()
        children = tree.get_children(node)
        if children:
            first_child = children[0]
            if tree.item(first_child, "text") == "Loading...":
                tree.delete(first_child)
                path = self._get_full_path(tree, node)
                self._populate_tree(tree, node, path)

    def _get_full_path(self, tree, node):
        parts = []
        while node:
            parts.append(tree.item(node, "text"))
            node = tree.parent(node)
        parts.reverse()
        return os.path.join(*parts)


    # Placeholder: create other frames for other buttons
    def create_search_frame(self):
        frame = tk.Frame(self.parent.window, width=200, bg="black")
        tk.Label(frame, text="Search Panel", fg="white", bg="black").pack(padx=10, pady=10)
        return frame

    def create_settings_frame(self):
        frame = tk.Frame(self.parent.window, width=200, bg="black")
        tk.Label(frame, text="Settings Panel", fg="white", bg="black").pack(padx=10, pady=10)
        return frame