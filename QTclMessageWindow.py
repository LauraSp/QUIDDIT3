import traceback
import tkinter as tk
from QTclPopupWindow import QTclPopupWindow

class QTclMessageWindow(QTclPopupWindow):
    """special message window for use in QUIDDIT
    """
    
    def __init__(self, parent, title, user_title, user_message, exc = None):
        """initialize the message box with a title, a user title, a username and and optinal with an exception
            With an exception the messagebox transforms into an error message box
        """
        self.user_message = user_message
        self.user_title = user_title
        self.exc = exc

        super().__init__(parent, title, is_modal=True) #message boxes are always modal
        

    def make_gui(self, title):
        self.setwintitle(title)

        row = 0
        titlab = self.makelabel(caption=self.user_title, sticky=tk.W, cspan = 2, padx=(5,5), pady=(5,5))
        titlab.configure(font=("TkCaptionFont", 18))
        row += 1
        self.makelabel(lrow=row, caption=self.user_message, cspan = 2, sticky=tk.W,padx=(5,5), pady=(0,5))
        row += 1        
        if self.exc != None:
            self.bu_row = row
            self.det_bu = self.makebutton(erow=row, ecol=1, caption="show details", cmd=self.show_details, 
                sticky=tk.E)
            row += 2

        if self.user_message.endswith('?') and self.exc==None:
            self.add_std_buttons(yescol=1, nocol=0, row=row)
        else:
            self.add_std_buttons(okcol=1, row=row)

    def show_details(self):
        details_txt = self.maketext(lrow=self.bu_row + 1, erow=self.bu_row + 1,  caption="error details:",
            lcol=0, ecol=1,
            width=100, height=30,
            padx=(5,5), pady=(5,5))
        details_txt.insert(tk.INSERT, self.get_exc_inf())
        details_txt.configure(state=tk.DISABLED)
        self.det_bu.configure(state=tk.DISABLED)

    def get_exc_inf(self):
        return traceback.format_exc()

    def loaded(self):
        pass
