# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:49:44 2019

@author: Laura
"""

from QImpWindowBasics import *
from QSettings import *
        

class QAskSpectraWindow(QTclPopupWindow):
    def __init__(self, parent, title, specs, is_modal=True):
        self.spec_files = specs
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def loaded(self):
        pass
    
    def make_gui(self, title):
        self.setwintitle(title)
        
        w=24
        row = 0
        lfr = self.make_label_frame(lrow=row, lcol=0, caption='Select spectra', cspan=2, padx=(5,5), pady=(5,5))
        
        irow = 0
        self.selfilesentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption="Spectra:", width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_spectra, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_file_num()

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)
        
    def do_nothing(self):
        pass

    def get_spectra(self):
        self.spec_files = fd.askopenfilenames(parent = self,
                                                initialdir = QSettings.userhome,
                                                title="Select spectra",
                                                filetypes=(('CSV','*.CSV'),('CSV','*.csv')))
        self.set_file_num()
    
    def set_file_num(self):
        self.selfilesentry.configure(state=tk.NORMAL)
        self.set_entry_text(self.selfilesentry, "{} files".format(len(self.spec_files)))
        self.selfilesentry.configure(state=tk.DISABLED)
        