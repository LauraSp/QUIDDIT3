from QImpWindowBasics import *

class QTclPopupWindow(QTclWindowBasics, tk.Toplevel):
    """base class for all pop up  windows
    """

    def __init__(self, parent, title, is_modal=True):
        self.parent = parent
        self.root = parent.root
        self.row = 0
        super().__init__(parent, padx=5, pady=5)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.resizable(True, True)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
                                  
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.make_gui(title)
        self.focus_set()
        self.loaded()

        if is_modal:
            self.grab_set()
            self.wait_window(self)

    def setwintitle(self, title):
        """Sets the title of your main window
        """
        self.title(title)

    def loaded(self):
        raise TclWinBaseUsageException("Override me! Always override loaded method")

    def make_gui(self, title):
        raise TclWinBaseUsageException("Override me! Always override loaded method")        

    def add_std_buttons(self, okcol=None, cancelcol=None, dismisscol=None, row=None, padx=(5,5), pady=(5,5)):
        if row == None:
            raise "Missing in row"

        if okcol != None:
            self.bind('<Return>', self.ok_event)
            self.makebutton(erow=row, ecol=okcol,
                                 width=5,
                                 caption='OK',
                                 cmd=self.ok_pressed,
                                 sticky=tk.E,
                                 padx=padx,
                                 pady=pady)
        if cancelcol != None:
            self.bind('<Escape>', self.cancel_event)
            self.makebutton(erow=row, ecol=cancelcol,
                                 width=5,
                                 caption='Cancel',
                                 cmd=self.cancel_pressed,
                                 sticky=tk.W,
                                 padx=padx,
                                 pady=pady)

        if dismisscol != None:
            self.bind('<Escape>', self.cancel_event)
            self.makebutton(erow=row, ecol=dismisscol,
                                 width=5,
                                 caption='Dismiss',
                                 cmd=self.cancel_pressed,
                                 sticky=tk.W,
                                 padx=padx,
                                 pady=pady)

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def ok_pressed(self):
        self.dresult = "OK"
        self.destroy()

    def cancel_pressed(self):
        self.dresult = "CANCEL"
        self.destroy()

    def ok_event(self, event):
        self.ok_pressed()

    def cancel_event(self, event):
        self.cancel_pressed()