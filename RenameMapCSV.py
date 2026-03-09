import os
import shutil

import tkinter as tk
from tkinter import filedialog


class MapCSVRenamer:
    '''class to rename map CSV files based on their position in the map'''
    def __init__(self, filelist, nrows, ncolumns, step_x, step_y, origin):
        # filelist should be a list of full paths to CSV files
        self.filelist = sorted(filelist)
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.step_x = step_x
        self.step_y = step_y
        self.origin = origin

    def rename_files(self):
        # use the provided file list directly instead of walking a folder
        if len(self.filelist) != self.nrows * self.ncolumns:
            raise ValueError(
                'Number of files does not match number of '
                f'rows ({self.nrows}) and columns ({self.ncolumns})'
            )

        k = 0
        for i in range(self.nrows):
            x = self.origin[0] + i * self.step_x
            for j in range(self.ncolumns):
                y = self.origin[1] + j * self.step_y
                # destination directory is the directory containing the file
                filepath = os.path.dirname(self.filelist[k])
                newfilename = f'X{x} Y{y}.CSV'
                shutil.copy(
                    self.filelist[k], os.path.join(filepath, newfilename)
                    )
                k += 1


class MapCSVInputWindow(tk.Toplevel):
    '''class to get user input for renaming map CSV files'''
    def __init__(self, parent, title='Rename map CSV files', is_modal=True):
        super().__init__(parent, padx=5, pady=5)
        self.parent = parent
        self.title(title)

        # Position window offset from parent
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        # Handle window close button
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # Initialize variables
        self.loaded()

        # Build GUI
        self.make_gui(title)

        # Set focus and make modal if requested
        self.focus_set()
        if is_modal:
            self.grab_set()
            self.wait_window(self)

    def loaded(self):
        # store selected file paths as a single string separated by ';'
        self.files = tk.StringVar(value='')
        self.nrows = tk.IntVar(value=1)
        self.ncolumns = tk.IntVar(value=1)
        self.step_x = tk.DoubleVar(value=100.0)
        self.step_y = tk.DoubleVar(value=100.0)
        self.origin_x = tk.DoubleVar(value=0.0)
        self.origin_y = tk.DoubleVar(value=0.0)
        # update count label whenever files change
        try:
            # newer tkinter
            self.files.trace_add('write', lambda *args: self._on_files_changed())
        except AttributeError:
            # older tkinter
            self.files.trace('w', lambda *args: self._on_files_changed())

    def make_gui(self, title):

        # make label, entry and button for selecting files
        row = 0
        tk.Label(self, text='Select CSV files:').grid(
            row=row,
            column=0,
            sticky=tk.W
        )
        tk.Button(self, text='Browse', command=self.browse_files).grid(
            row=row,
            column=2,
            padx=(5, 5),
            pady=(0, 5)
        )
        # label that shows how many files are selected (placed in column 1)
        self.count_label = tk.Label(self, text='Selected: 0')
        self.count_label.grid(row=row, column=1, sticky=tk.W, padx=(5,5))

        # make labels and entries for number of rows and columns, step sizes,
        # and origin
        row += 1
        tk.Label(self,
                 text='Number of rows (x):').grid(row=row,
                                                  column=0,
                                                  sticky=tk.W)
        tk.Entry(self,
                 textvariable=self.nrows, width=10).grid(row=row, column=1)

        row += 1
        tk.Label(self,
                 text='Number of columns (y):').grid(row=row,
                                                     column=0,
                                                     sticky=tk.W)
        tk.Entry(self,
                 textvariable=self.ncolumns, width=10).grid(row=row, column=1)

        row += 1
        tk.Label(self,
                 text='Step size in x (microns):').grid(row=row,
                                                        column=0,
                                                        sticky=tk.W)
        tk.Entry(self,
                 textvariable=self.step_x, width=10).grid(row=row, column=1)

        row += 1
        tk.Label(self,
                 text='Step size in y (microns):').grid(row=row,
                                                        column=0,
                                                        sticky=tk.W)
        tk.Entry(self,
                 textvariable=self.step_y, width=10).grid(row=row, column=1)

        row += 1
        tk.Label(self,
                 text='Origin x (microns):').grid(row=row,
                                                  column=0,
                                                  sticky=tk.W)
        tk.Entry(self,
                 textvariable=self.origin_x, width=10).grid(row=row, column=1)

        row += 1
        tk.Label(self,
                 text='Origin y (microns):').grid(row=row,
                                                  column=0,
                                                  sticky=tk.W)
        tk.Entry(self,
                 textvariable=self.origin_y, width=10).grid(row=row, column=1)

        # add OK and Cancel buttons
        row += 1
        padx = (5, 5)
        pady = (5, 5)

        self.bind('<Return>', self.ok_event)
        tk.Button(self,
                  text='OK',
                  width=5,
                  command=self.ok_pressed).grid(row=row,
                                                column=0,
                                                sticky=tk.E,
                                                padx=padx,
                                                pady=pady)

        self.bind('<Escape>', self.cancel_event)
        tk.Button(self,
                  text='Cancel',
                  width=5,
                  command=self.cancel_pressed).grid(row=row,
                                                    column=1,
                                                    sticky=tk.W,
                                                    padx=padx,
                                                    pady=pady)

    def browse_files(self):
        """Open a file chooser and update the files variable."""
        selected = filedialog.askopenfilenames(
            parent=self,
            initialdir=self.files.get() or '.',
            title='Select CSV files',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')]
        )
        if selected:
            # join with semicolon so it can be stored in a StringVar
            self.files.set(';'.join(selected))

    def _on_files_changed(self):
        """Update the selected-files count label."""
        s = self.files.get()
        count = len([p for p in s.split(';') if p]) if s else 0
        if hasattr(self, 'count_label'):
            try:
                self.count_label.config(text=f'Selected: {count}')
            except Exception:
                pass

    def cancel(self, event=None):
        """Handle window close button"""
        self.parent.focus_set()
        self.destroy()

    def ok_pressed(self):
        """Handle OK button press"""
        self.dresult = "OK"
        self.destroy()

    def cancel_pressed(self):
        """Handle Cancel button press"""
        self.dresult = "CANCEL"
        self.destroy()

    def ok_event(self, event):
        """Handle Return key"""
        self.ok_pressed()

    def cancel_event(self, event):
        """Handle Escape key"""
        self.cancel_pressed()


if __name__ == "__main__":
    # use tkinter to enter number of rows and columns, step sizes,
    # and map origin and file list
    root = tk.Tk()
    root.withdraw()

    input_window = MapCSVInputWindow(root)
    files_str = input_window.files.get()
    filelist = [p for p in files_str.split(';') if p]
    nrows = input_window.nrows.get()
    ncolumns = input_window.ncolumns.get()
    step_x = input_window.step_x.get()
    step_y = input_window.step_y.get()
    origin = (input_window.origin_x.get(), input_window.origin_y.get())

    # rename files
    renamer = MapCSVRenamer(filelist, nrows, ncolumns, step_x, step_y, origin)
    renamer.rename_files()
