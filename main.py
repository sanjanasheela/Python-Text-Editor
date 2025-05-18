import tkinter as tk
from tkinter import filedialog

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Text Editor")
        self.window.geometry("900x600")

        # Frame to hold line numbers and text area
        self.editor_frame = tk.Frame(self.window)
        self.editor_frame.pack(fill="both", expand=True)

        # Line numbers area
        self.line_numbers = tk.Text(self.editor_frame, width=4, padx=4, takefocus=0, border=0,
                                    background='lightgrey', state='disabled', wrap='none')
        self.line_numbers.pack(side="left", fill="y")

        # Main text area
        self.text_area = tk.Text(self.editor_frame, wrap="word", undo=True)
        self.text_area.pack(side="right", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.on_scroll)
        self.scrollbar.pack(side="right", fill="y")

        # Event binding to update line numbers
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<ButtonRelease-1>", self.update_line_numbers)

        self.create_menu()
        self.update_line_numbers()

        self.window.mainloop()

    def on_scroll(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)

        row_count = int(self.text_area.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, row_count))
        self.line_numbers.insert(tk.END, line_numbers_string)
        self.line_numbers.config(state='disabled')

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.update_line_numbers()

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.window.title(f"Python Text Editor - {file}")
            self.text_area.delete(1.0, tk.END)
            with open(file, "r") as file_handler:
                self.text_area.insert(tk.INSERT, file_handler.read())
            self.update_line_numbers()

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            with open(file, "w") as file_handler:
                file_handler.write(self.text_area.get(1.0, tk.END))
            self.window.title(f"Python Text Editor - {file}")

    def create_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

if __name__ == "__main__":
    TextEditor()
