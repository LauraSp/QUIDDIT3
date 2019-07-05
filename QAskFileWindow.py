from QImpWindowBasics import *
from QSettings import *
from QTclMessageWindow import *
        

class QAskFileWindow(QTclPopupWindow):
    def __init__(self, parent, title, caption, sel_file, is_modal=True):
        self.sel_file = sel_file
        self.dresult = "NONE"
        self.caption = caption
        super().__init__(parent, title, is_modal)


    def loaded(self):
        pass
    
    def make_gui(self, title):
        self.setwintitle(title)
        
        w=44
        row = 0
        lfr = self.make_label_frame(lrow=row, lcol=0, caption='Select file', cspan=2, padx=(5,5), pady=(5,5))
        
        irow = 0
        self.selfileentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption=self.caption+':', width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_file, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_entry_text(self.selfileentry, self.sel_file)

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)


    def get_file(self):
        selfilevar = fd.askopenfilename(parent = self,
                    initialdir = QSettings.userhome,
                    title="Select file",
                    filetypes=(('CSV','*.CVS'),('CSV','*.csv'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.selfileentry, selfilevar)


    def ok_pressed(self):
        self.sel_file = self.selfileentry.get()
        super().ok_pressed()