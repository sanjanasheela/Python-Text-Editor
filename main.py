import tkinter as tk
from tkinter import ttk, filedialog
from MenuBar import MenuBar  # your MenuBar code stays the same
from ActivityBar import ActivityBar

class TextEditor:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Text Editor")
        self.window.geometry("900x600")

        self.window.configure(bg="black")

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True)

        # Inside main_frame:
        self.activity_bar_frame = tk.Frame(self.main_frame, width=80, bg="white")
        self.activity_bar_frame.pack(side="left", fill="y")

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side="right", fill="both", expand=True)

        # Add first new tab on start
        self.new_text_file()



        # Bind tab changed event to update line numbers for active tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)


        # Menu Bar
        self.menu_bar = MenuBar(self)

        # activity Bar


        self.window.mainloop()

    def create_editor_tab(self, content="", title="Untitled"):
        frame = tk.Frame(self.notebook,bg="black")

        # Line numbers text widget
        line_numbers = tk.Text(frame, width=4, padx=4,bd=0,highlightthickness=0, takefocus=0, border=0, background='black',fg='white', state='disabled', wrap='none')
        line_numbers.pack(side="left", fill="y")

        # Main text widget
        text_area = tk.Text(frame, wrap="word", undo=True, bg="black", fg="white",insertbackground="white")
        text_area.pack(side="right", fill="both", expand=True)

        text_area.focus_set()

        # Scrollbar linked to text_area and line_numbers
        scrollbar = tk.Scrollbar(text_area)
        scrollbar.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self._on_scroll(text_area, line_numbers))

        # Insert content if any
        if content:
            text_area.insert(tk.END, content)

        # Bind events to update line numbers on edits and scroll
        text_area.bind("<KeyRelease>", lambda e: self.update_line_numbers(text_area, line_numbers))
        text_area.bind("<MouseWheel>", lambda e: self.update_line_numbers(text_area, line_numbers))
        text_area.bind("<ButtonRelease-1>", lambda e: self.update_line_numbers(text_area, line_numbers))

        # Initialize line numbers
        self.update_line_numbers(text_area, line_numbers)

        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

        return frame, text_area, line_numbers

    def _on_scroll(self, text_widget, line_numbers_widget):
        def on_scroll(*args):
            text_widget.yview(*args)
            line_numbers_widget.yview(*args)
        return on_scroll

    def update_line_numbers(self, text_widget, line_numbers_widget):
        line_numbers_widget.config(state='normal')
        line_numbers_widget.delete(1.0, tk.END)
        row_count = int(text_widget.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, row_count))
        line_numbers_widget.insert(tk.END, line_numbers_string)
        line_numbers_widget.config(state='disabled')

    def get_current_tab_widgets(self):
        current_tab = self.notebook.select()
        if not current_tab:
            return None, None, None
        frame = self.notebook.nametowidget(current_tab)
        children = frame.winfo_children()
        # children[0] = line_numbers, children[1] = text_area
        if len(children) < 2:
            return None, None, None
        return frame, children[1], children[0]

    def new_text_file(self):
        self.create_editor_tab()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            filename = file_path.split("/")[-1]
            self.create_editor_tab(content=content, title=filename)

    def save_as_file(self):
        frame, text_area, line_numbers = self.get_current_tab_widgets()
        if not text_area:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file_handler:
                file_handler.write(text_area.get(1.0, tk.END))
            filename = file_path.split("/")[-1]
            tab_index = self.notebook.index(self.notebook.select())
            self.notebook.tab(tab_index, text=filename)
            self.window.title(f"Python Text Editor - {filename}")

    def open_new_window(self):
        # Opens a brand new TextEditor window (independent)
        TextEditor()

    def on_tab_changed(self, event):
        frame, text_area, line_numbers = self.get_current_tab_widgets()
        if text_area and line_numbers:
            self.update_line_numbers(text_area, line_numbers)

if __name__ == "__main__":
    TextEditor()


