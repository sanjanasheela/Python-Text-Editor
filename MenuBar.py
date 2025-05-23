import tkinter as tk
import subprocess
# from shell import CShellConsole


class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.menu = tk.Menu(self.parent.window)
        self.parent.window.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Text File", command=self.parent.new_text_file)
        # self.file_menu.add_command(label="New File", command=self.parent.new_file)
        self.file_menu.add_command(label="New Window", command=self.parent.open_new_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Open File", command=self.parent.open_file)
        # self.file_menu.add_command(label="Open Folder", command=self.open_file)
        # self.file_menu.add_command(label="Open Workspace from File", command=self.open_file)
        # self.file_menu.add_command(label="Open Recent", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.parent.save_as_file)
        self.file_menu.add_command(label="Save As", command=self.parent.save_as_file)
        self.file_menu.add_separator()
        # self.file_menu.add_command(label="Revert File", command=self.open_new_window)
        self.file_menu.add_command(label="Close Editor", command=self.close_current_tab)
        # self.file_menu.add_command(label="Close Folder", command=self.open_new_window)
        self.file_menu.add_command(label="Close Window", command=self.close_current_window)
        # self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.parent.window.quit)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        # self.edit_menu.add_command(label="Undo", command=self.undo)
        # self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        # self.edit_menu.add_command(label="Find", command=self.find_word)
        # self.edit_menu.add_command(label="Replace", command=self.replace)
        self.edit_menu.add_separator()
        # self.edit_menu.add_command(label="Find in Files", command=self.find_in_files)
        # self.edit_menu.add_command(label="Replace in Files", command=self.replace_in_files)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Toggle Line Comments", command=self.toggle_comment)
        self.edit_menu.add_command(label="Toggle Block Comments", command=self.toggle_block_comment)
        # self.edit_menu.add_command(label="Expand Abbreviations", command=self.expand_abbreviations)

        # Selection menu
        self.selection_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="selection", menu=self.selection_menu)
        self.selection_menu.add_command(label="Select All", command=self.select_all)
        self.selection_menu.add_command(label="Expand Selection", command=self.expand_selection)
        self.selection_menu.add_command(label="Shrink Selection", command=self.shrink_selection)
        self.selection_menu.add_separator()
        self.selection_menu.add_command(label="Copy Line Up", command=self.copy_line_up)
        self.selection_menu.add_command(label="Copy Line Down", command=self.copy_line_down)
        self.selection_menu.add_command(label="Move Line Up", command=self.move_line_up)
        self.selection_menu.add_command(label="Move Line Down", command=self.move_line_down)
        self.selection_menu.add_command(label="Duplicate Selection", command=self.duplicate_selection)
        self.selection_menu.add_separator()
        # self.selection_menu.add_command(label="Add Cursors Above", command=self.add_cursor_above)
        # self.selection_menu.add_command(label="Add Cursors Below", command=self.add_cursor_below)
        # self.selection_menu.add_command(label="Add Cursor to Line Ends", command=self.add_cursor_to_line_ends)
        self.selection_menu.add_command(label="Add Next Occurrence", command=self.add_next_occurrence)
        self.selection_menu.add_command(label="Add Previous Occurrence", command=self.add_previous_occurrence)
        self.selection_menu.add_command(label="Select All Occurrences", command=self.select_all_occurrences)
        self.selection_menu.add_separator()
        # self.selection_menu.add_command(label="Switch to Ctrl+Click for Multicursors", command=self.switch_to_ctrl_click)
        # self.selection_menu.add_command(label="Column Selection Mode", command=self.column_selection_mode)

        # Other top-level menus
        self.menu.add_cascade(label="View", menu=tk.Menu(self.menu, tearoff=0))
        self.menu.add_cascade(label="Go", menu=tk.Menu(self.menu, tearoff=0))

        self.run_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Code", command=self.run_code)
        # self.run_menu.add_command(label="Run File", command=self.run_file)

        self.selection_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Terminal", menu=self.selection_menu)
        # self.selection_menu.add_command(label="open terminal",command=self.parent.open_cshell_tab)

        self.menu.add_cascade(label="Help", menu=tk.Menu(self.menu, tearoff=0))



    # Placeholder methods
    def cut(self,event=None):
        frame, text_area, line_numbers = self.parent.get_current_tab_widgets()
        if text_area:
            try:
                selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.parent.window.clipboard_clear()
                self.parent.window.clipboard_append(selected_text)
                text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            except tk.TclError:
                pass  # No text selected

    def copy(self,event=None):
        frame,text_area,line_numbers = self.parent.get_current_tab_widgets()
        if text_area:
            try:
                selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.parent.window.clipboard_clear()
                self.parent.window.clipboard_append(selected_text)
            except tk.TclError:
                pass


    def paste(self,event=None):
        try:
            self.parent.text_area.event_generate("<<Paste>>")
        except AttributeError:
            pass

    def run_code(self):
        current_tab = self.parent.notebook.select()
        frame = self.parent.notebook.nametowidget(current_tab)
        text_widget = frame.winfo_children()[1]  # assuming order [line_numbers, text_area]

        if hasattr(text_widget, 'full_path'):
            print("Running:", text_widget.full_path)
            code = text_widget.get("1.0", tk.END)
            # Save and run logic here


        if not frame.path:
            print("Please save the file before running.")
            return

        # Run it using subprocess
        process = subprocess.Popen(
            ['python3', frame.path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if stdout:
            print("Output:\n", stdout)
        if stderr:
            print("Error:\n", stderr)

    def close_current_window(self):
        self.parent.window.destroy()

    def close_current_tab(self):
        current_tab = self.parent.notebook.select()
        if current_tab:
            self.parent.notebook.forget(current_tab)


    def toggle_comment(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())

        children = current_tab.winfo_children()
        text_widget = None
        for child in children:
            if isinstance(child, tk.Text) and child.cget("state") != "disabled":
                text_widget = child
                break

        if not text_widget:
            return

        # Try to get selection, otherwise use current line
        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
        except tk.TclError:
            start_index = text_widget.index("insert linestart")
            end_index = text_widget.index("insert lineend")

        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])

        # Check if all lines are commented
        all_commented = True
        lines_text = []
        for line in range(start_line, end_line + 1):
            line_start = f"{line}.0"
            line_end = f"{line}.end"
            line_text = text_widget.get(line_start, line_end)
            lines_text.append(line_text)
            if not line_text.lstrip().startswith("#"):
                all_commented = False

        # Now toggle based on all_commented
        for i, line in enumerate(range(start_line, end_line + 1)):
            line_start = f"{line}.0"
            line_end = f"{line}.end"
            line_text = lines_text[i]

            if all_commented:
                # Uncomment: remove first '#' after leading spaces
                stripped = line_text.lstrip()
                hash_index = line_text.find("#")
                if hash_index != -1:
                    new_text = line_text[:hash_index] + line_text[hash_index + 1:]
                else:
                    new_text = line_text
            else:
                # Comment: add '#' after leading spaces
                leading_spaces = len(line_text) - len(line_text.lstrip())
                new_text = line_text[:leading_spaces] + "#" + line_text[leading_spaces:]

            text_widget.delete(line_start, line_end)
            text_widget.insert(line_start, new_text)

        return "break"

    def toggle_block_comment(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        children = current_tab.winfo_children()
        text_widget = None
        for child in children:
            if isinstance(child, tk.Text) and child.cget("state") != "disabled":
                text_widget = child
                break

        if not text_widget:
            return

        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
            has_selection = True
        except tk.TclError:
            start_index = text_widget.index("insert linestart")
            end_index = text_widget.index("insert lineend")
            has_selection = False

        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])

        # Get the full text of selection
        content = text_widget.get(f"{start_line}.0", f"{end_line}.end")

        # Check if content already wrapped in triple quotes
        stripped = content.strip()
        if stripped.startswith('"""') and stripped.endswith('"""'):
            # Remove the triple quotes
            new_content = stripped[3:-3].strip('\n')
            text_widget.delete(f"{start_line}.0", f"{end_line}.end")
            text_widget.insert(f"{start_line}.0", new_content)
            return

        # Otherwise, add triple quotes
        if has_selection and start_line != end_line:
            # Insert """ at start and end of the block
            text_widget.insert(f"{start_line}.0", '"""' + '\n')
            text_widget.insert(f"{end_line + 2}.0", '\n"""')  # +2 to account for inserted """ line
        else:
            # No selection or same line: wrap line with triple quotes
            line_text = text_widget.get(f"{start_line}.0", f"{start_line}.end")
            if line_text.strip().startswith('"""') and line_text.strip().endswith('"""'):
                new_line = line_text.strip()[3:-3]
                text_widget.delete(f"{start_line}.0", f"{start_line}.end")
                text_widget.insert(f"{start_line}.0", new_line)
            else:
                new_line = f'"""{line_text}"""'
                text_widget.delete(f"{start_line}.0", f"{start_line}.end")
                text_widget.insert(f"{start_line}.0", new_line)

    def select_all(self, event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        children = current_tab.winfo_children()
        text_widget = None
        for child in children:
            if isinstance(child, tk.Text) and child.cget("state") != "disabled":
                text_widget = child
                break

        if text_widget:
            text_widget.tag_add("sel", "1.0", "end-1c")  # Select all text
            text_widget.mark_set("insert", "end-1c")  # Move cursor to end
            text_widget.see("insert")  # Scroll to cursor
        return "break"  # Prevent default behavior if bound to a key event

    def expand_selection(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        children = current_tab.winfo_children()
        text_widget = None
        for child in children:
            if isinstance(child, tk.Text) and child.cget("state") != "disabled":
                text_widget = child
                break

        if not text_widget:
            return

        try:
            start = text_widget.index("sel.first")
            end = text_widget.index("sel.last")
        except tk.TclError:
            # If no selection, expand current line
            start = text_widget.index("insert linestart")
            end = text_widget.index("insert lineend")

        start_line = max(int(start.split('.')[0]) - 1, 1)
        end_line = int(end.split('.')[0]) + 1

        new_start = f"{start_line}.0"
        new_end = f"{end_line}.end"
        text_widget.tag_remove("sel", "1.0", "end")
        text_widget.tag_add("sel", new_start, new_end)
        text_widget.see(new_end)

    def shrink_selection(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        children = current_tab.winfo_children()
        text_widget = None
        for child in children:
            if isinstance(child, tk.Text) and child.cget("state") != "disabled":
                text_widget = child
                break

        if not text_widget:
            return

        try:
            start = text_widget.index("sel.first")
            end = text_widget.index("sel.last")
        except tk.TclError:
            return  # Nothing selected to shrink

        start_line = int(start.split('.')[0])
        end_line = int(end.split('.')[0])

        if end_line - start_line <= 1:
            return  # Too small to shrink further

        new_start = f"{start_line + 1}.0"
        new_end = f"{end_line - 1}.end"
        text_widget.tag_remove("sel", "1.0", "end")
        text_widget.tag_add("sel", new_start, new_end)
        text_widget.see(new_end)

    def copy_line_up(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
            has_selection = True
        except tk.TclError:
            start_index = text_widget.index("insert linestart")
            end_index = text_widget.index("insert lineend")
            has_selection = False

        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])

        lines = text_widget.get(f"{start_line}.0", f"{end_line}.end")

        text_widget.insert(f"{start_line}.0", lines + "\n")

    def copy_line_down(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
            has_selection = True
        except tk.TclError:
            start_index = text_widget.index("insert linestart")
            end_index = text_widget.index("insert lineend")
            has_selection = False

        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])

        lines = text_widget.get(f"{start_line}.0", f"{end_line}.end")

        text_widget.insert(f"{end_line + 1}.0", lines + "\n")

    def move_line_up(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
        except tk.TclError:
            start_index = text_widget.index("insert linestart")
            end_index = text_widget.index("insert lineend")

        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])

        if start_line == 1:
            return  # Can't move above the first line

        above_line_text = text_widget.get(f"{start_line - 1}.0", f"{start_line - 1}.end")
        selected_text = text_widget.get(f"{start_line}.0", f"{end_line}.end")

        text_widget.delete(f"{start_line - 1}.0", f"{end_line}.end")
        text_widget.insert(f"{start_line - 1}.0", selected_text + '\n' + above_line_text)

        text_widget.tag_remove("sel", "1.0", "end")
        text_widget.tag_add("sel", f"{start_line - 1}.0", f"{end_line - 1}.end")

    def move_line_down(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
        except tk.TclError:
            start_index = text_widget.index("insert linestart")
            end_index = text_widget.index("insert lineend")

        start_line = int(start_index.split('.')[0])
        end_line = int(end_index.split('.')[0])
        last_line = int(text_widget.index("end-1c").split('.')[0])

        if end_line >= last_line:
            return  # Can't move beyond the last line

        below_line_text = text_widget.get(f"{end_line + 1}.0", f"{end_line + 1}.end")
        selected_text = text_widget.get(f"{start_line}.0", f"{end_line}.end")

        text_widget.delete(f"{start_line}.0", f"{end_line + 1}.end")
        text_widget.insert(f"{start_line}.0", below_line_text + '\n' + selected_text)

        text_widget.tag_remove("sel", "1.0", "end")
        text_widget.tag_add("sel", f"{start_line + 1}.0", f"{end_line + 1}.end")

    def duplicate_selection(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            start_index = text_widget.index("sel.first")
            end_index = text_widget.index("sel.last")
            selected_text = text_widget.get(start_index, end_index)
            text_widget.insert(end_index, selected_text)
            text_widget.tag_remove("sel", "1.0", "end")
            text_widget.tag_add("sel", end_index, f"{end_index} + {len(selected_text)} chars")
        except tk.TclError:
            # No selection, duplicate current line
            line_start = text_widget.index("insert linestart")
            line_end = text_widget.index("insert lineend")
            line_text = text_widget.get(line_start, line_end)
            text_widget.insert(line_end, '\n' + line_text)

    def add_previous_occurrence(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            sel_start = text_widget.index("sel.first")
            sel_end = text_widget.index("sel.last")
        except tk.TclError:
            return  # No initial selection

        selected_text = text_widget.get(sel_start, sel_end)
        if not selected_text.strip():
            return  # Ignore blank selections

        # Initialize custom tag style if not already done
        text_widget.tag_configure("multi_sel", background="skyblue")

        # Convert all current multi_sel tagged ranges
        ranges = text_widget.tag_ranges("multi_sel")
        if ranges:
            # Get all current (start, end) tuples
            sel_ranges = list(zip(ranges[::2], ranges[1::2]))

            # Find earliest selection to search backward from
            earliest_start = min(sel_ranges, key=lambda pair: text_widget.index(pair[0]))[0]

            # Ensure all existing selections match the current selected text
            for start, end in sel_ranges:
                if text_widget.get(start, end) != selected_text:
                    text_widget.tag_remove("multi_sel", "1.0", "end")
                    sel_ranges = []
                    earliest_start = sel_start
                    break
        else:
            sel_ranges = []
            earliest_start = sel_start

        # Search backward for previous occurrence
        prev_start = text_widget.search(selected_text, earliest_start, stopindex="1.0",
                                        backwards=True, nocase=False, exact=True)
        if not prev_start:
            return

        prev_end = f"{prev_start}+{len(selected_text)}c"

        # Avoid duplicate selections
        if any(text_widget.compare(prev_start, "==", start) for start, _ in sel_ranges):
            return

        # Add previous match using custom tag
        text_widget.tag_add("multi_sel", prev_start, prev_end)

    def clear_multi_selections(self):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text)), None)
        if text_widget:
            text_widget.tag_remove("multi_sel", "1.0", "end")

    def add_next_occurrence(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            sel_start = text_widget.index("sel.first")
            sel_end = text_widget.index("sel.last")
        except tk.TclError:
            return  # No selection

        selected_text = text_widget.get(sel_start, sel_end)
        if not selected_text.strip():
            return

        # Initialize custom tag style if not already done
        text_widget.tag_configure("multi_sel", background="skyblue")

        # Get all existing multi_sel ranges
        ranges = text_widget.tag_ranges("multi_sel")
        if ranges:
            sel_ranges = list(zip(ranges[::2], ranges[1::2]))

            # Check that all selections are for the same text
            for start, end in sel_ranges:
                if text_widget.get(start, end) != selected_text:
                    text_widget.tag_remove("multi_sel", "1.0", "end")
                    sel_ranges = []
                    latest_end = sel_end
                    break
            else:
                # Use the furthest selection to search forward from
                latest_end = max(sel_ranges, key=lambda pair: text_widget.index(pair[1]))[1]
        else:
            sel_ranges = []
            latest_end = sel_end

        # Search forward from the latest end
        next_start = text_widget.search(selected_text, latest_end, stopindex="end",
                                        forwards=True, nocase=False, exact=True)
        if not next_start:
            return

        next_end = f"{next_start}+{len(selected_text)}c"

        # Avoid duplicate selections
        if any(text_widget.compare(next_start, "==", start) for start, _ in sel_ranges):
            return

        # Add to multi-selection
        text_widget.tag_add("multi_sel", next_start, next_end)

    def select_all_occurrences(self,event=None):
        current_tab = self.parent.notebook.nametowidget(self.parent.notebook.select())
        text_widget = next((child for child in current_tab.winfo_children()
                            if isinstance(child, tk.Text) and child.cget("state") != "disabled"), None)
        if not text_widget:
            return

        try:
            sel_start = text_widget.index("sel.first")
            sel_end = text_widget.index("sel.last")
        except tk.TclError:
            return  # No selection made

        selected_text = text_widget.get(sel_start, sel_end)
        if not selected_text.strip():
            return  # Ignore blank selections

        # Configure the multi_sel tag if not already configured
        text_widget.tag_configure("multi_sel", background="skyblue")

        # Remove any previous multi selections
        text_widget.tag_remove("multi_sel", "1.0", "end")

        # Start searching from the beginning of the text
        start_pos = "1.0"
        while True:
            match_start = text_widget.search(selected_text, start_pos, stopindex="end",
                                             nocase=False, exact=True)
            if not match_start:
                break
            match_end = f"{match_start}+{len(selected_text)}c"
            text_widget.tag_add("multi_sel", match_start, match_end)
            start_pos = match_end  # Move to the end of the current match

    # not able to add the toggle line shortcut
    def bind_shortcuts(self):
        self.parent.window.bind("<Control-Shift-N>", self.parent.open_new_window)
        self.parent.window.bind("<Control-n>", self.parent.new_text_file)
        self.parent.window.bind("<Control-o>", self.parent.open_file)
        self.parent.window.bind("<Control-Shift-S>", self.parent.save_as_file)
        self.parent.window.bind("<Control-W>", self.close_current_tab)
        self.parent.window.bind("<Alt-F4>", self.close_current_window)
        self.parent.window.bind("<Control-q>", self.parent.window.quit)# this is not working

        self.parent.window.bind("<Control-x>", self.cut)
        self.parent.window.bind("<Control-c>", self.copy)
        self.parent.window.bind("<Control-v>", self.paste)
        self.parent.window.bind("<Control-Shift-A>", self.toggle_block_comment)

        self.parent.window.bind("<Control-a>", self.select_all)
        self.parent.window.bind("<Control-Alt-Shift-Up>", self.copy_line_up)#not working
        self.parent.window.bind("<Control-Alt-Shift-Down>", self.copy_line_down)#not working
        self.parent.window.bind("<Alt-Up>", self.move_line_up)
        self.parent.window.bind("<Alt-Down>", self.move_line_down)
        self.parent.window.bind("<Control-Shift-Left>", self.shrink_selection)
        self.parent.window.bind("<Control-Shift-Right>", self.expand_selection)
        self.parent.window.bind("<Control-d>", self.add_next_occurrence)#not working
        self.parent.window.bind("<Control-Shift-D>", self.add_previous_occurrence)
        self.parent.window.bind("<Control-Shift-L>", self.select_all_occurrences)

        self.parent.window.bind("<Control-F5>",self.run_code)