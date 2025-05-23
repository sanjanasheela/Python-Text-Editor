import tkinter as tk
from tkinter import ttk, filedialog
from MenuBar import MenuBar  # your MenuBar code stays the same
from ActivityBar import ActivityBar
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
import keyword
import re
import builtins
import subprocess
import os

class TextEditor:

    def __init__(self,master=None):
        self.window = tk.Toplevel(master) if master else tk.Tk()
        self.window.title("Python Text Editor")
        self.window.geometry("900x600")
        self.window.configure(bg="black")

        self.path = os.getcwd()
        print(self.path)
        # Activity Bar (left side)
        self.activity_bar = ActivityBar(self)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(side="right", fill="both", expand=True)

        # Add first new tab on start
        self.new_text_file(self.path)

        # Bind tab changed event to update line numbers for active tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Menu Bar
        self.menu_bar = MenuBar(self)
        self.menu_bar.bind_shortcuts()

        self.multi_selections = []  # list of (start_index, end_index)


        if not master:
            self.window.mainloop()




    def create_editor_tab(self, content="", title="Untitled",path=""):
        frame = tk.Frame(self.notebook,bg="black")
        frame.path = path
        print("h")
        print(path)

        # Close button on top-right inside the frame
        # close_btn = tk.Button(frame, text="✕", command=lambda: self.close_tab(frame),
        #                       bg="black", fg="white", bd=0, padx=5, pady=2,
        #                       font=("Arial", 12, "bold"))
        # close_btn.pack(side="top", anchor="ne", padx=2, pady=2)
        # Line numbers text widget
        line_numbers = tk.Text(frame, width=4, padx=4,bd=0,highlightthickness=0, takefocus=0, border=0, background='black',fg='white', state='disabled', wrap='none')
        line_numbers.pack(side="left", fill="y")

        # Main text widget
        text_area = tk.Text(frame, wrap="none", undo=True, bg="black", fg="white",insertbackground="white")
        text_area.pack(side="right", fill="both", expand=True)



        # Apply the scrollbar with this style
        scrollbar = ttk.Scrollbar(text_area, style='Custom.Vertical.TScrollbar')
        scrollbar.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self._on_scroll(text_area, line_numbers))

        horscrollbar = ttk.Scrollbar(text_area, orient="horizontal", style='Custom.Horizontal.TScrollbar')
 # You can define a horizontal style if you want
        horscrollbar.pack(side="bottom", fill="x")
        text_area.config(xscrollcommand=horscrollbar.set)
        horscrollbar.config(command=text_area.xview)

        # Insert content if any
        if content:

            text_area.insert(tk.END, content)

        # Configure syntax highlighting
        lexer = PythonLexer()
        style = get_style_by_name("monokai")

        for ttype, n in style:
            if n['color']:
                text_area.tag_configure(str(ttype), foreground=f"#{n['color']}")

        def highlight(event=None):
            text = text_area.get("1.0", tk.END)

            # Clear old tags
            for tag in text_area.tag_names():
                text_area.tag_remove(tag, "1.0", tk.END)

            # Highlight keywords
            for kw in keyword.kwlist:
                for match in re.finditer(rf"\b{kw}\b", text):
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    text_area.tag_add("keyword", start, end)

            # Highlight strings and store spans to avoid highlighting inside them
            string_spans = []
            for match in re.finditer(r'(\".*?\"|\'.*?\')', text):
                start_idx, end_idx = match.start(), match.end()
                string_spans.append((start_idx, end_idx))
                start = f"1.0 + {start_idx} chars"
                end = f"1.0 + {end_idx} chars"
                text_area.tag_add("string", start, end)

            # Highlight comments outside strings
            for match in re.finditer(r'#.*', text):
                start_idx = match.start()
                if not any(start <= start_idx < end for start, end in string_spans):
                    start = f"1.0 + {start_idx} chars"
                    end = f"1.0 + {match.end()} chars"
                    text_area.tag_add("comment", start, end)\

            block_comment_pattern = r'("""(.|\n)*?"""|\'\'\'(.|\n)*?\'\'\')'
            for match in re.finditer(block_comment_pattern, text):
                start_idx, end_idx = match.start(), match.end()
                start = f"1.0 + {start_idx} chars"
                end = f"1.0 + {end_idx} chars"
                text_area.tag_add("comment", start, end)

            builtin_funcs = [name for name in dir(builtins) if callable(getattr(builtins, name))]
            for func in builtin_funcs:
                for match in re.finditer(rf"\b{func}\b", text):
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    text_area.tag_add("function", start, end)
            # Find all function names defined by 'def'
            function_names = []
            for match in re.finditer(r'\bdef (\w+)', text):
                fname = match.group(1)
                function_names.append(fname)
                # Highlight the definition itself
                start = f"1.0 + {match.start(1)} chars"
                end = f"1.0 + {match.end(1)} chars"
                text_area.tag_add("function", start, end)

            # Now highlight all occurrences of these function names (calls or mentions)
            for fname in function_names:
                # Use word boundaries to avoid partial matches
                for match in re.finditer(rf'\b{re.escape(fname)}\b', text):
                    start_idx = match.start()
                    # Skip if inside strings or comments
                    if any(start <= start_idx < end for start, end in string_spans):
                        continue
                    # You could also skip inside comments if you want
                    # For now, let's highlight everywhere except strings
                    start = f"1.0 + {match.start()} chars"
                    end = f"1.0 + {match.end()} chars"
                    text_area.tag_add("function", start, end)



            # Configure tags with colors
            text_area.tag_configure("keyword", foreground="blue")
            text_area.tag_configure("function", foreground="yellow")
            text_area.tag_configure("string", foreground="orange")
            text_area.tag_configure("comment", foreground="green")

        # Bind highlighting
            def on_text_change(event):
                    text_widget = event.widget  # the Text widget that triggered this
                    if text_widget.edit_modified():
                        text_widget.edit_modified(False)  # reset the modified flag

                        # Now call your update functions:
                        self.update_line_numbers(text_widget, line_numbers)
                        highlight()

            text_area.bind("<<Modified>>", on_text_change)
            text_area.bind("<MouseWheel>", lambda e: self.update_line_numbers(text_area, line_numbers))
            text_area.bind("<ButtonRelease-1>", lambda e: self.update_line_numbers(text_area, line_numbers))


        # Initial update
        self.update_line_numbers(text_area, line_numbers)
        highlight()

        # Add tab
        self.notebook.add(frame, text=title)

        self.notebook.select(frame)
        self.window.title(f"Python Text Editor - {title}")
        self.window.update()


        return frame, text_area, line_numbers

    def get_active_text_widget(self):
        current_tab = self.notebook.nametowidget(self.notebook.select())
        for child in current_tab.winfo_children():
            if isinstance(child, tk.Text) and child.cget("state") != "disabled":
                return child
        return None

    def new_text_file(self,event=None):
        self.create_editor_tab()

    def open_new_window(self,event=None):
        # Opens a brand new TextEditor window (independent)
        TextEditor(master=self.window)

    def open_file(self,event=None):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                           filetypes=[("All files", "*.*"),("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            filename = file_path.split("/")[-1]
            self.create_editor_tab(content=content, title=filename,path=file_path)



    def save_as_file(self,event=None):
        frame, text_area, line_numbers = self.get_current_tab_widgets()
        if not text_area:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file_handler:
                file_handler.write(text_area.get(1.0, tk.END))
            filename = file_path.split("/")[-1]
            tab_index = self.notebook.index(self.notebook.select())
            self.notebook.tab(tab_index, text=filename)
            self.window.title(f"Python Text Editor - {filename}")
            frame.path = file_path

    def close_tab(self, frame):
        self.notebook.forget(frame)
    def _on_scroll(self, text_widget, line_numbers_widget):
        def on_scroll(*args):
            text_widget.yview(*args)
            line_numbers_widget.yview(*args)
        return on_scroll

    def on_tab_changed(self, event):
        frame, text_area, line_numbers = self.get_current_tab_widgets()
        if text_area and line_numbers:
            self.update_line_numbers(text_area, line_numbers)

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



if __name__ == "__main__":
    TextEditor()



